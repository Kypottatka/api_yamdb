from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from api.serializers import CommentSerializer, ReviewSerializer
from reviews.models import Review, Comment, Title


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
