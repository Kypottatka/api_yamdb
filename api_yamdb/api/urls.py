from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

v1_router = DefaultRouter()
v1_router.register('categories', CategoriesViewSet, basename='categories')
v1_router.register('genres',
                   GenresViewSet, basename='genres')
v1_router.register('titles', TitlesViewSet, basename='titles')


urlpatterns = [
    path('v1/', include(v1_router.urls))
],
urlpatterns = [
    path('v1/', include('users.urls')),
]
