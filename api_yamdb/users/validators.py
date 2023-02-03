import re

from django.core.exceptions import ValidationError
from django.conf import settings


def username_validator(username):
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise ValidationError(
            'Имя пользователя может содержать '
            'только латинские буквы, цифры и символ подчеркивания.'
        )
    if len(username) < 3:
        raise ValidationError(
            'Имя пользователя должно быть не короче 3 символов.'
        )
    if len(username) > settings.USER_USERNAME_LENGTH:
        raise ValidationError(
            'Имя пользователя должно быть не длиннее 150 символов.'
        )
