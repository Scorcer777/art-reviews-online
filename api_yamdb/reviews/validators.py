import re

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
