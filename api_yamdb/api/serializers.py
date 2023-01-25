from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Categories, Genres, Titles, Review, Comment

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


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    @staticmethod
    def validate_score(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError('Оценка по 10-бальной шкале!')
        return value

    class Meta:
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=(
                    "title",
                    "author",
                ),
            ),
        ]
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ("rate",)
