from django.db.models import Avg
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from users.permissions import (
    AdminOrReadOnly,
    IsAdminModeratorAuthorOrReadOnly,
)
from .filtersets import TitleFilter
from .mixins import CreateListViewSet
from .pagination import CustomPagination
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    CommentSerializer,
    ReviewSerializer,
    TitleListSerializer,
    TitleCreateSerializer,
)
from reviews.models import Category, Genre, Title, Review


class CategoryViewSet(CreateListViewSet):
    """
    Вьюсет для обработки [GET, POST, DELETE] запросов
    к объектам модели Category.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListViewSet):
    """
    Вьюсет для обработки [GET, POST, DELETE] запросов
    к объектам модели Genre.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для обработки [GET, POST, PATCH, DELETE] запросов
    к объектам модели Title.
    """

    queryset = Title.objects.annotate(rating=Avg("reviews__score"))
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering = ("name",)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleListSerializer
        return TitleCreateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для обработки [GET, POST, PATCH, DELETE] запросов
    к объектам модели Review.
    """

    serializer_class = ReviewSerializer
    permission_classes = (
        IsAdminModeratorAuthorOrReadOnly,
        IsAuthenticatedOrReadOnly,
    )
    pagination_class = CustomPagination

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для обработки [GET, POST, PATCH, DELETE] запросов
    к объектам модели Comment.
    """

    serializer_class = CommentSerializer
    permission_classes = (
        IsAdminModeratorAuthorOrReadOnly,
        IsAuthenticatedOrReadOnly,
    )
    pagination_class = CustomPagination

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
