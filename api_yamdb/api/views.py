from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.permissions import IsAdminOrReadOnly
from .pagination import CustomPagination
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer, CommentSerializer, ReviewSerializer
from reviews.models import Category, Genre, Title, Review, Comment
from .mixins import CreateListViewSet


class CategoryViewSet(CreateListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = CustomPagination


class GenreViewSet(CreateListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = CustomPagination
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    ordering_fields = ('name',)
    pagination_class = CustomPagination


class ReviewViewSet(viewsets.ModelViewSet):
    """
        Вьюсет для обработки [GET, POST, PUT, PATCH, DELETE] запросов
        к объектам модели Review.
    """

    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.select_related("author", "title").only(
            "id", "text", "author__username", "title__id"
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
        Вьюсет для обработки [GET, POST, PUT, PATCH, DELETE] запросов
        к объектам модели Comment.
    """

    serializer_class = CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(
            Review,
            id=review_id
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)

    def perform_destroy(self, serializer):
        comment_id = self.kwargs.get("comment_id")
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()
