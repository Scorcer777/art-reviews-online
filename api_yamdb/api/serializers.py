from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.validators import username_validator, validate_year


class UserSerializer(serializers.ModelSerializer):
    '''Вывод данных о пользователях.'''
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[
            username_validator,
            UniqueValidator(queryset=User.objects.all()),
        ]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role',
        )


class SignUpSerializer(serializers.ModelSerializer):
    '''Обработка данных для регистрации.'''
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[
            username_validator,
        ]
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
    )

    class Meta:
        model = User
        fields = ('username', 'email',)


class GenerateTokenSerializer(serializers.ModelSerializer):
    """Обработка данных для генерации токена."""
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[username_validator]
    )
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)


class CategorySerializer(serializers.ModelSerializer):
    """Обработка данных для категорий."""
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    """Обработка данных для жанров."""
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleReadSerializer(serializers.ModelSerializer):
    """Обработка данных для чтения произведений."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True,
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year',
            'rating', 'description',
            'genre', 'category',
        )


class TitlePostSerializer(serializers.ModelSerializer):
    """Обработка данных для добавления произведений."""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all(),
    )
    year = serializers.IntegerField(validators=[validate_year],)

    class Meta:
        model = Title
        fields = (
            'id', 'name',
            'year', 'description',
            'genre', 'category',
        )


class ReviewSerializer(serializers.ModelSerializer):
    '''Обработка данных для отзывов.'''
    author = serializers.StringRelatedField(
        required=False,
    )
    score = serializers.IntegerField(
        min_value=1,
        max_value=10,
    )
    pub_date = serializers.DateTimeField(
        read_only=True,
        required=False,
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, value):
        request = self.context['request']
        title = get_object_or_404(
            Title,
            id=self.context['view'].kwargs['title_id'],
        )
        if (
            request.method == 'POST'
            and request.user.reviews.all().exists()
        ):
            raise serializers.ValidationError('Вы уже оставляли отзыв здесь.')
        return value


class CommentSerializer(serializers.ModelSerializer):
    '''Обработка данных для комментариев.'''
    author = serializers.StringRelatedField(required=False)
    pub_date = serializers.DateTimeField(
        read_only=True,
        required=False,
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
