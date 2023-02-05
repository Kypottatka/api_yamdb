import datetime

from django.core.exceptions import ValidationError
from django.conf import settings


def username_validator(username):
    if (username == 'me'
       or username == 'Me'
       or username == 'ME'
       or username == 'mE'):
        raise ValidationError(
            'Имя пользователя не может быть "me".'
        )
    if len(username) < 3:
        raise ValidationError(
            'Имя пользователя должно быть не короче 3 символов.'
        )
    if len(username) > settings.USER_USERNAME_LENGTH:
        raise ValidationError(
            'Имя пользователя должно быть не длиннее 150 символов.'
        )


def year_validator(year):
    if year < 0 or year > datetime.datetime.now().year:
        raise ValidationError(
            'Год должен быть в диапазоне от 0 до текущего года.'
        )
