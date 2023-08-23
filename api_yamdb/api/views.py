from django.db import IntegrityError
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from reviews.models import Title, User
from api.serializers import TitleSerializer, SignUpSerializer

EMAIL = 'test@yandex.ru'


class SignUpView(APIView):
    '''Обрабатка запроса на регистрацию нового пользователя.'''
    permission_classes = (AllowAny,)

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
            ValidationError(
                'Поля "email" и "username" должны быть уникальными'
            )

        confirmation_code = default_token_generator.make_token(user)

        send_mail(
            'Код для подтверждения регистрации',
            f'Ваш код подтверждения: "{confirmation_code}".',
            EMAIL,
            [email],
            fail_silently=False,
        )

        return Response(
            {'email': email, 'username': username},
            status=status.HTTP_200_OK
        )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = [DjangoFilterBackend]
