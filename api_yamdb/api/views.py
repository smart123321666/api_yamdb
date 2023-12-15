from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, viewsets
from rest_framework import mixins
from rest_framework.pagination import LimitOffsetPagination

from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReviewSerializer,
    CommentSerializer
)

# from api.permissions import IsAuthenticatedAuthororReadOnly
from reviews.models import Category, Genre, Review, Title, Genre
from api.permissions import IsAuthenticatedAuthororReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedAuthororReadOnly,)
    pagination_class = LimitOffsetPagination
    # pass


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    #permission_classes = (IsAuthenticatedAuthororReadOnly,)
    #pagination_class = LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAuthenticatedAuthororReadOnly,)
    pagination_class = LimitOffsetPagination


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedAuthororReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_titlet(self):
        return self.get_review().reviews.all()

    def perform_create(self, serializer):
        return serializer.save(
            #author=self.request.user,
            post=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedAuthororReadOnly,)

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


"""class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedAuthororReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user
        )


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedAuthororReadOnly,)

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            post=self.get_post()
        )


class Followviewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.follows.all()

    def perform_create(self, serializer):
        return serializer.save(
            user=self.request.user
        ) """