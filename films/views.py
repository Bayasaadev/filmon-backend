from rest_framework import viewsets
from .models import Film, Genre, Studio, Streaming, Tag
from .serializers import (
    FilmSerializer,
    GenreSerializer,
    StudioSerializer,
    StreamingSerializer,
    TagSerializer
)
from .permissions import IsStaffOrReadOnly
from artists.models import FilmArtistRole

class FilmViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all().prefetch_related(
        'genres', 'studios', 'tags',
        'film_roles__artist'
    ).order_by('-created_at')
    serializer_class = FilmSerializer
    permission_classes = [IsStaffOrReadOnly]


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
