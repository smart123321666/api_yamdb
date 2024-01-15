
import django_filters
from api.permissions import IsAdmin, IsOwner, ReadOnly
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleSerializer, TitleSerializerCreateUpdate)
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from django.db.models import Avg, F

from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitleSerializerCreateUpdate,
    ReviewSerializer,
    CommentSerializer
)

from api.permissions import ReadOnly, IsAdmin, IsOwner
from api.filtres import TitleFilter
from rest_framework.response import Response
from reviews.models import Category, Genre, Review, Title


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):


class CustomPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class TitleFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter()
    name = django_filters.CharFilter(
        lookup_expr='icontains'
    )
    category = django_filters.CharFilter(
        field_name='category__slug',
        lookup_expr='contains'
    )
    genre = django_filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='icontains'
    )

    class Meta:
        model = Title
        fields = ['year', 'name', 'category', 'genre']


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdmin,)
    permission_classes = (IsAdmin,)
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'list':
            return (ReadOnly(),)
        return super().get_permissions()


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'list':
            return (ReadOnly(),)
        return super().get_permissions()


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdmin,)
    permission_classes = (IsAdmin,)
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'list':
            return (ReadOnly(),)
        return super().get_permissions()
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'list':
            return (ReadOnly(),)
        return super().get_permissions()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg(F('reviews__score'))
    )
    permission_classes = (IsAdmin,)
    queryset = Title.objects.all()
    serializer_class = TitleSerializerCreateUpdate
    permission_classes = (IsAdmin,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'list':
            return (ReadOnly(),)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializer
        return TitleSerializerCreateUpdate

    def perform_update(self, serializer):
        instance = serializer.save()
        reviews = Review.objects.filter(title=instance)
        if reviews.exists():
            rating = reviews.aggregate(Avg('score'))['score__avg']
            instance.rating = round(rating, 2)
            instance.save()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsOwner,)
    http_method_names = ['get', 'post', 'head', 'delete', 'patch']
    permission_classes = (IsOwner,)
    pagination_class = CustomPagination
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
    permission_classes = (IsOwner,)
    pagination_class = CustomPagination
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
            author=self.request.user,
            review=self.get_review()
        )
