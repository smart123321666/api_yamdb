from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg, F
from django.shortcuts import get_object_or_404
from rest_framework import (filters, mixins, permissions,
                            status, views, viewsets)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django_filters.rest_framework import DjangoFilterBackend

from api.filtres import TitleFilter
from api.permissions import IsAdmin, IsOwner, IsAdminOrReadOnly
from api.serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer,
    ReviewSerializer, TitleSerializer, TitleSerializerCreateUpdate,
    CodeConfirmSerializer, CustomUserCreationSerializer, CustomUserSerializer
)
from reviews.models import Category, Genre, Review, Title
from api.viewsets import CustomBaseViewSet

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    search_fields = ['username']

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(data=serializer.data)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(data=serializer.data)


class UserSignUpView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = CustomUserCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        existing_user_by_email = User.objects.filter(email=email).first()
        existing_user_by_username = User.objects.filter(username=username).first()

        if existing_user_by_email != existing_user_by_username:
            error_msg = {}
            if existing_user_by_email != None and existing_user_by_username != None:
                error_msg = {'email': ['Пользователь с таким email уже существует.'], 'username': ['Пользователь с таким username уже существует.']}
            if existing_user_by_email != None:
                error_msg = {'email': ['Пользователь с таким email уже существует.']}
            if existing_user_by_username != None:
                error_msg = {'email': ['Пользователь с таким username уже существует.']}
            return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)

        user, _ = User.objects.get_or_create(email=email, username=username)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Code confirmation',
            message=f'Your confirmation code is: {confirmation_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
            )
        return Response({'email': email, 'username': username}, status=status.HTTP_200_OK)




class TokenObtainView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = CodeConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(CustomBaseViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CustomBaseViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg(F('reviews__score'))
    )
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializer
        return TitleSerializerCreateUpdate


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsOwner,)
    http_method_names = ['get', 'post', 'head', 'delete', 'patch']

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwner,)
    http_method_names = ['get', 'post', 'head', 'delete', 'patch']

    def get_review(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
