from django.core.exceptions import ValidationError
from django.conf import settings


def username_validator(username):
    username = username.lower()
    if username == 'me':
        raise ValidationError(
            'Имя пользователя не может быть "me".'
        )
    if len(username) < 3:
        raise ValidationError(
            'Имя пользователя должно быть не короче 3 символов.'
        )
    if len(username) > settings.USER_FIELD_LENGTH:
        raise ValidationError(
            'Имя пользователя должно быть не длиннее 150 символов.'
        )
