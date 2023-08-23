from django.urls import include, path
from rest_framework import routers

from api.views import TitleViewSet, SignUpView

router_v1 = routers.DefaultRouter()

router_v1.register(r'titles', TitleViewSet)

urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/', include(router_v1.urls))
]
