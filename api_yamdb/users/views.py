from http import HTTPStatus
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import IsAdmin
from .serializers import (CodeConfirmSerializer, CustomUserCreationSerializer,
                          CustomUserSerializer)
from rest_framework.pagination import LimitOffsetPagination

User = get_user_model()


class CustomPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class UserViewSet(viewsets.ModelViewSet):
    queryset= User.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ['get','post','patch','delete']
    permission_classes = (IsAdmin,)
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    search_fields = ['username']

    @action(detail=False, methods=['get','patch'],
            permission_classes=[permissions.IsAuthenticated])
    def me(self,request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(data=serializer.data)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data = request.data,
                partial = True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(data=serializer.data)

class UserSignUpView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        existing_user = User.objects.filter(email=email).first()
        existing_email = User.objects.filter(username=username).first()
        if existing_user and existing_email:
                return Response({'email': existing_user.email, 'username': existing_email.username}, status=status.HTTP_200_OK)
        serializer = CustomUserCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(username=username)
            user = User.objects.get(username=username)
            user.is_active = False
            user.save()
            send_mail(subject='Code confirmation',
                      message=f'Your confirmation is: {user.confirmation_code}',
                      from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[email],
                      fail_silently=False)

            return Response({'email': email, 'username': username}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TokenObtainView(views.APIView):
    permission_classes=(permissions.AllowAny,)

    def post(self, request):
        serializer = CodeConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)
        if user and confirmation_code == user.confirmation_code:
            user.is_active = True
            user.save()
            token = AccessToken.for_user(user)
            return Response({'token':f'{token}'},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)