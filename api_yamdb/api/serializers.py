from datetime import date
from rest_framework import serializers
from reviews.models import Category, Genre, Title, Review, Comment


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели Category."""

    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели Genre."""

    class Meta:
        model = Genre
        fields = ("name", "slug")


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        write_only=True,
        slug_field="slug",
        required=False,
        queryset=Genre.objects.all(),
    )
    category = serializers.SlugRelatedField(
        many=False,
        write_only=True,
        slug_field="slug",
        required=False,
        queryset=Category.objects.all(),
    )

    def validate_year(self, value):
        if not 0 < value < date.today().year:
            raise serializers.ValidationError(
                f"Пока мы в {date.today().year}, пользователь уже в {value}"
            )
        return value

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
        )


class TitleListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, required=False)
    genre = GenreSerializer(many=True, required=False)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )
        read_only_fields = ("genre", "category", "rating")


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")

    def validate(self, data):
        is_exist = Review.objects.filter(
            author=self.context["request"].user,
            title=self.context["view"].kwargs.get("title_id"),
        ).exists()
        if is_exist and self.context["request"].method == "POST":
            raise serializers.ValidationError(
                "Вы уже оставляли отзыв на это произведение."
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )
    review = serializers.SlugRelatedField(
        slug_field="text",
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = "__all__"
