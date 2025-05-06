from rest_framework import viewsets
from .models import Artist, FilmArtistRole
from .serializers import ArtistSerializer, FilmArtistRoleSerializer
from films.permissions import IsStaffOrReadOnly  # Reuse staff-only write access

class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all().order_by('full_name')
    serializer_class = ArtistSerializer
    permission_classes = [IsStaffOrReadOnly]


class FilmArtistRoleViewSet(viewsets.ModelViewSet):
    queryset = FilmArtistRole.objects.select_related('film', 'artist')
    serializer_class = FilmArtistRoleSerializer
    permission_classes = [IsStaffOrReadOnly]
