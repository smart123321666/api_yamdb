from django.urls import include, path
from rest_framework import routers

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    # UserViewSet
)

app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register(
    'categories',
    CategoryViewSet,
    basename='categorie'
)
v1_router.register(
    'genres',
    GenreViewSet,
    basename='genre'
)
v1_router.register(
    'titles',
    TitleViewSet,
    basename='title'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)}/comments',
    CommentViewSet,
    basename='comment'
)
""" v1_router.register(
    'users',
    UserViewSet,
    basename='user'
) """

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    # path('v1/', include('djoser.urls.jwt')),
]
