from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet, TokenObtainView,
                       UserSignUpView, UserViewSet)
from django.urls import include, path
from rest_framework import routers

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
v1_router.register(
    'users',
    UserViewSet,
    basename='users'
)


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', UserSignUpView.as_view(), name='signup'),
    path('v1/auth/token/', TokenObtainView.as_view(), name='token_obtain'),
]
