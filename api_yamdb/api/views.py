import django_filters
from django.shortcuts import get_object_or_404
from rest_framework import  viewsets, filters
# from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination

from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReviewSerializer,
    CommentSerializer
)

from reviews.models import Category, Genre, Review, Title
from api.permissions import IsAdminOrReadOnly,IsOwner


class CustomPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class TitleFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter()
    name = django_filters.CharFilter(
        lookup_expr='icontains'
    )
    category = django_filters.CharFilter(
        field_name='category__name',
        lookup_expr='contains'
    )
    genre = django_filters.CharFilter(
        field_name='genre__name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Title
        fields = ['year', 'name', 'category', 'genre']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAuthenticatedAuthororReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsOwner,)
    pagination_class = CustomPagination

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        return serializer.save(
            #author=self.request.user,
            post=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwner,)
    pagination_class = CustomPagination

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        return serializer.save(
            #author=self.request.user,
            post=self.get_review()
        )


class UserViewSet(viewsets.ModelViewSet):
    pass
