from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import TitleFilter
from api.permissions import (IsAdmin, IsAdminOrReadOnly,
                             PermissionsForReviewsAndComments)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenerateTokenSerializer, GenreSerializer,
                             ReviewSerializer, SignUpSerializer,
                             TitlePostSerializer, TitleReadSerializer,
                             UserSerializer, )
from reviews.models import Category, Genre, Review, Title, User
from django.conf import settings


class UserViewSet(viewsets.ModelViewSet):
    '''Вывод информации о пользователях.'''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=('GET', 'PATCH'),
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        '''Получение или изменение информации о себе.'''
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            # Страхуемся от изменения пользовательской роли.
            if serializer.validated_data.get('role'):
                serializer.validated_data['role'] = request.user.role
            serializer.save()
            return Response(serializer.data)

        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class SignUpView(APIView):
    '''Обрабатка запроса на регистрацию нового пользователя.'''

    def post(self, request):
        '''Обработка POST-запроса.'''
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')

        try:
            user, created = User.objects.get_or_create(
                email=email,
                username=username,
            )
        except IntegrityError:
            raise ValidationError(
                'Поля "email" и "username" должны быть уникальными'
            )

        confirmation_code = default_token_generator.make_token(user)

        send_mail(
            'Код для подтверждения регистрации',
            f'Ваш код подтверждения: "{confirmation_code}".',
            settings.EMAIL,
            [email],
            fail_silently=False,
        )

        return Response(
            {'email': email, 'username': username},
            status=status.HTTP_200_OK,
        )


class GenerateTokenView(APIView):
    '''Создание токена.'''

    def post(self, request):
        serializer = GenerateTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)

        if default_token_generator.check_token(
            user,
            confirmation_code,
        ):
            token = str(AccessToken.for_user(user))
            return Response(
                {'token': token},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TitleViewSet(viewsets.ModelViewSet):
    '''
    Вывод действий с произведениями.
    Для запросов на чтения используется TitleReadSerializer.
    Для запросов на редактирования используется TitlePostSerializer.
    '''
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    )
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitlePostSerializer


class CategoryAndGenreMixin(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Миксин для CategoryViewSet и GenreViewSet."""
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name']
    lookup_field = 'slug'


class CategoryViewSet(CategoryAndGenreMixin):
    '''Вывод действий с жанрами.'''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryAndGenreMixin):
    '''Вывод действий с жанрами.'''
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewset(viewsets.ModelViewSet):
    '''Вывод действий с отзывами.'''
    serializer_class = ReviewSerializer
    permission_classes = (PermissionsForReviewsAndComments,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'),
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'),
        )
        serializer.save(
            title=title,
            author=self.request.user,
        )


class CommentViewset(viewsets.ModelViewSet):
    '''Вывод действий с комментариями.'''
    serializer_class = CommentSerializer
    permission_classes = (PermissionsForReviewsAndComments,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
        )
        serializer.save(
            review=review,
            author=self.request.user,
        )
