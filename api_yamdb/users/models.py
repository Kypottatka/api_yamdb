from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core import validators


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = [
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
]


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        new_user = self.model(
            email=email,
            **kwargs
        )

        new_user.set_password(password)
        new_user.save()
        return new_user

    def create_superuser(self, email, password, **kwargs):
        new_user = self.model(
            email=email,
            is_staff=True,
            is_superuser=True,
            **kwargs
        )

        new_user.set_password(password)
        new_user.save()
        return new_user


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Никнейм пользователя',
        max_length=150,
        unique=True,
        db_index=True,
        validators=[validators.RegexValidator(
            regex=r'^[\w.@+-]+\Z',
            message='Имя пользователя должно состоять '
                    'только из букв латинского алфавита, '
                    'цифр и символов "@/./+/-/_"',
            code='invalid_username',
        )],
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=254,
        unique=True,
        validators=[validators.validate_email],
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=150,
        choices=ROLES,
        default=USER,
    )
    bio = models.TextField(
        verbose_name='О себе',
        null=True,
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=150,
        null=True,
    )
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def is_admin(self):
        return (self.role == ADMIN
                or self.is_staff or self.is_superuser)

    def is_moderator(self):
        return (self.role == MODERATOR
                or self.is_staff or self.is_superuser)

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        unique_together = (('username', 'email'),)
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    def __str__(self) -> str:
        return self.username
