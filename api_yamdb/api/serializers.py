from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Title, User
from reviews.validators import username_validator


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[username_validator],
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')


class SignUpSerializer(serializers.Serializer):
    '''Обработка данных для регистрации.'''
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[
            username_validator,
            UniqueValidator(queryset=User.objects.all()),
        ]
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all()),],
    )

    class Meta:
        model = User
        fields = ('username', 'email')


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = '__all__'
