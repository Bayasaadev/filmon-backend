from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import FilmFilter
from .models import Film, Genre, Studio, Streaming, Tag
from .serializers import (
    FilmSerializer,
    GenreSerializer,
    StudioSerializer,
    StreamingSerializer,
    TagSerializer
)
from .permissions import IsStaffOrReadOnly

class FilmViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.annotate(
        average_score=Avg('user_data__rating')
    ).prefetch_related(
        'genres', 'tags', 'studios', 'streamings', 'film_role__artist'
    )
    serializer_class = FilmSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = FilmFilter
    search_fields = ['title', 'description', 'tagline']
    ordering_fields = ['release_date', 'created_at', 'title', 'duration', 'average_score']
    ordering = ['-release_date']


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsStaffOrReadOnly]


class StudioViewSet(viewsets.ModelViewSet):
    queryset = Studio.objects.all()
    serializer_class = StudioSerializer
    permission_classes = [IsStaffOrReadOnly]


class StreamingViewSet(viewsets.ModelViewSet):
    queryset = Streaming.objects.all()
    serializer_class = StreamingSerializer
    permission_classes = [IsStaffOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsStaffOrReadOnly]
