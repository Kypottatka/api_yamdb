from django.contrib import admin

from .models import Categories, Genres, Titles


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('slug',)
    list_filter = ('slug',)


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('slug',)
    list_filter = ('slug',)


@admin.register(Titles)
class TitlesAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'category',
    )
    search_fields = ('name',)
    list_filter = ('category',)
