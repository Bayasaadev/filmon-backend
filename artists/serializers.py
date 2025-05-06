from rest_framework import serializers
from .models import Artist, FilmArtistRole

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = [
            'id', 'full_name', 'bio',
            'birth_date', 'nationality', 'photo'
        ]


class FilmArtistRoleSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    film = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = FilmArtistRole
        fields = [
            'id', 'film', 'artist',
            'role_type', 'character_name', 'order'
        ]
