from django.contrib.auth import get_user_model

from rest_framework import viewsets, filters
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import CategorySerializer, GenreSerializer, TitleSerializer, CommentSerializer, ReviewSerializer
from reviews.models import Category, Genre, Title, Review, Comment

User = get_user_model()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (AllowAny,)


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
