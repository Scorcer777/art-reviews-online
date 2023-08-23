from django.contrib.auth.models import AbstractUser
from django.db import models

# Пользовательские роли.
ROLES = [
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
]


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
    )
    first_name = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        null=True,
    )
    role = models.CharField(
        max_length=256,
        verbose_name='Роль',
        choices=ROLES,
        default='user',
    )

    class Meta:
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Title(models.Model):
    name = models.CharField(
        'Название',
        max_length=256,
    )
    year = models.IntegerField('Год выпуска')
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'объект "Произведение"'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
