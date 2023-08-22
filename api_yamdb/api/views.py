from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from reviews.models import Title
from api.serializers import TitleSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = [DjangoFilterBackend]
