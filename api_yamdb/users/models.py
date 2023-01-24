from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    status = models.CharField(
        max_length=30,
        choices=(
            ('user', 'Пользователь'),
            ('moderator', 'Модератор'),
            ('admin', 'Администратор'),
        ),
        default='user',
        verbose_name='Статус пользователя',
    )
