from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

from .validators import username_validator


USER = "user"
MODERATOR = "moderator"
ADMIN = "admin"

ROLES = [
    (USER, "Пользователь"),
    (MODERATOR, "Модератор"),
    (ADMIN, "Администратор"),
]


class User(AbstractUser):
    username = models.CharField(
        verbose_name="Никнейм пользователя",
        max_length=settings.USER_USERNAME_LENGTH,
        unique=True,
        db_index=True,
        validators=[username_validator],
    )
    email = models.EmailField(
        verbose_name="Электронная почта",
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=150,
        blank=True,
    )
    role = models.CharField(
        verbose_name="Роль",
        max_length=150,
        choices=ROLES,
        default=USER,
    )
    bio = models.TextField(
        verbose_name="О себе",
        null=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_user(self):
        return self.role == USER

    class Meta:
        ordering = ("username",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        unique_together = (("username", "email"),)
        constraints = [
            models.UniqueConstraint(
                fields=["username", "email"], name="unique_username_email"
            )
        ]

    def __str__(self) -> str:
        return self.username
