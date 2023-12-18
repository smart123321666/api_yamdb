from django.urls import include, path
from rest_framework import routers

from api.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
)

app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register(
    'categories',
    CategoryViewSet,
    basename='category'
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
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
v1_router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
