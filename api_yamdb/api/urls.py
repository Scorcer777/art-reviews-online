from django.urls import include, path
from rest_framework import routers

from api.views import (
    CategoryViewSet, CommentViewset, GenreViewSet,
    ReviewViewset, SignUpView, TitleViewSet, UserViewSet,
    GenerateTokenView
)

router_v1 = routers.DefaultRouter()

router_v1.register(
    'users',
    UserViewSet,
    basename='users',
)
router_v1.register(
    'categories',
    CategoryViewSet,
    basename='categories',
)
router_v1.register(
    'genres',
    GenreViewSet,
    basename='genres',
)
router_v1.register(
    'titles',
    TitleViewSet,
    basename='titles',
)
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewset,
    basename='reviews',
)
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/$',
    ReviewViewset,
    basename='review',
)
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewset, basename='comments')


urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', GenerateTokenView.as_view()),
    path('v1/', include(router_v1.urls))
]
