from rest_framework.routers import DefaultRouter
from .views import FilmUserDataViewSet, ReviewViewSet, CustomListViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'film-user-data', FilmUserDataViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'custom-lists', CustomListViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
