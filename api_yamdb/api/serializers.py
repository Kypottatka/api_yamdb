from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Review, Comment


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