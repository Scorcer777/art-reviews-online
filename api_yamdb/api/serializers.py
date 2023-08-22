from rest_framework import serializers

from reviews.models import Title


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = '__all__'
