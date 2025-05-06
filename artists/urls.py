from rest_framework.routers import DefaultRouter
from .views import ArtistViewSet, FilmArtistRoleViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'artists', ArtistViewSet)
router.register(r'roles', FilmArtistRoleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
