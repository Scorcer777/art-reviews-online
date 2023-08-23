from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from reviews.models import Title, User, Review, Comment
from reviews.validators import username_validator


class ReviewSerializer(serializers.ModelSerializer):
    '''Обработка данных для отзывов.'''
    author = serializers.StringRelatedField(required=False)
    score = serializers.IntegerField(min_value=1,
                                     max_value=10)
    pub_date = serializers.DateTimeField(read_only=True,
                                         required=False)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
                message='Вы можете оставить только один отзыв к произведению.'
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    '''Обработка данных для комментариев.'''
    author = serializers.StringRelatedField(required=False)
    pub_date = serializers.DateTimeField(read_only=True,
                                         required=False)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


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
        validators=[UniqueValidator(queryset=User.objects.all()), ],
    )

    class Meta:
        model = User
        fields = ('username', 'email')


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = '__all__'
