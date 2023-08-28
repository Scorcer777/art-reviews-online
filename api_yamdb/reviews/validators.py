import re
from datetime import datetime

from django.core.exceptions import ValidationError


def username_validator(value):
    if value.lower() == 'me':
        raise ValidationError(
            'Использовать имя "me" в качестве `username` запрещено'
        )

    if re.search(r'^[\w.@+-]+$', value) is None:
        raise ValidationError(
            'Недопустимые символы в имени пользователя'
        )


def validate_year(value):
    now = datetime.now().year
    if value > now:
        raise ValidationError(
            f'{value} год не может быть больше текущего {now} года'
        )
