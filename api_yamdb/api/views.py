from django.contrib.auth import get_user_model

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from .serializers import CategoriesSerializer, GenresSerializer, TitlesSerializer
from api_yamdb.api_yamdb.reviews.models import Categories, Genres, Titles

User = get_user_model()


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.Searchfilter,)
    search_fields = ('name',)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.Searchfilter,)
    search_fields = ('name',)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (IsAuthenticated,)
