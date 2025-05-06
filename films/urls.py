from rest_framework.routers import DefaultRouter
from .views import (
    FilmViewSet, GenreViewSet, StudioViewSet,
    StreamingViewSet, TagViewSet
)
from django.urls import path, include

router = DefaultRouter()
router.register(r'films', FilmViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'studios', StudioViewSet)
router.register(r'streamings', StreamingViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
