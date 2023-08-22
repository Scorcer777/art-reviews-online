from django.urls import include, path
from rest_framework import routers

from api.views import TitleViewSet

router = routers.DefaultRouter()

router.register(r'titles', TitleViewSet)

urlpatterns = [
    path('v1/', include(router.urls))
]
