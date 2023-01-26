from django.contrib import admin

from .models import Category, Genre, Title


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('slug',)
    list_filter = ('slug',)


@admin.register(Genre)
class GenresAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('slug',)
    list_filter = ('slug',)


@admin.register(Title)
class TitlesAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'category',
    )
    search_fields = ('name',)
    list_filter = ('category',)
