from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Genre, Title, User, Review, Comment
from reviews.validators import username_validator, validate_year


class UserSerializer(serializers.ModelSerializer):
    '''Вывод данных о пользователях.'''
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[username_validator],
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
        
        
class GenerateTokenSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = Category
        exclude = ('id', )


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id', )


class TitleReadSerializer(serializers.ModelSerializer):
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
            'genre', 'category')


class TitlePostSerializer(serializers.ModelSerializer):
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
            'genre', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    '''Обработка данных для отзывов.'''
    author = serializers.StringRelatedField(
        required=False
    )
    score = serializers.IntegerField(
        min_value=1,
        max_value=10
    )
    pub_date = serializers.DateTimeField(
        read_only=True,
        required=False
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
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
    pub_date = serializers.DateTimeField(
        read_only=True,
        required=False
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
