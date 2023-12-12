from django.urls import include, path
from rest_framework import routers

from .views import CommentViewSet, Followviewset, GroupViewSet, PostViewSet

app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register(
    'posts',
    PostViewSet,
    basename='post'
)
v1_router.register(
    'groups',
    GroupViewSet,
    basename='group'
)
v1_router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)
v1_router.register(
    'follow',
    Followviewset,
    basename='follow'
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/', include('djoser.urls.jwt')),
]