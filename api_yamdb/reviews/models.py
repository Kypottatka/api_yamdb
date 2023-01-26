from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название',
                            help_text='Заполните имя категории')
    slug = models.SlugField(max_length=50, unique=True,
                            help_text='Поле с уникальным значением')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категория'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название',
                            help_text='Заполните имя жанра')
    slug = models.SlugField(max_length=50, unique=True,
                            help_text='Поле с уникальным значением')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанры'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название',
                            help_text='Заполните название произведения')
    year = models.IntegerField(
        verbose_name='Год выпуска', help_text='Заполните год выпуска')
    description = models.TextField(blank=True, null=True,
                                   verbose_name='описание',
                                   help_text='Заполните описание')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL, blank=True,
        null=True, related_name='titles',
        verbose_name='категория',
        help_text='Выберите категорию'
    )
    genre = models.ManyToManyField(
        Genre, blank=True,
        related_name='genre',
        verbose_name='жанр',
        help_text='Выберите один или несколько жанров'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведения'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
