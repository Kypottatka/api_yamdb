from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import Categories, Genres, Titles

User = get_user_model()


class CategoriesSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(slug_field='name',
                                        read_only=True)

    class Meta:
        fields = '__all__'
        exclude = ('id',)
        model = Categories


class GenresSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(slug_field='name',
                                        read_only=True)

    class Meta:
        fields = '__all__'
        exclude = ('id',)
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(slug_field='name',
                                        read_only=True)
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(), slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(), slug_field='slug'
    )

    class Meta:
        fields = '__all__'
        model = Titles
