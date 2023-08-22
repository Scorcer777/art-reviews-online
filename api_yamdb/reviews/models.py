from django.db import models


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
