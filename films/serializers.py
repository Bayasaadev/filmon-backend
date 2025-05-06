from rest_framework import serializers
from .models import (
    Genre, Studio, Streaming, Tag,
    Film, FilmStreaming
)
from artists.models import FilmArtistRole
from artists.serializers import ArtistSerializer


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug']


class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = ['id', 'name', 'country', 'founded_year', 'description']


class StreamingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Streaming
        fields = ['id', 'name', 'logo']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class FilmStreamingSerializer(serializers.ModelSerializer):
    streaming = StreamingSerializer()

    class Meta:
        model = FilmStreaming
        fields = ['id', 'streaming', 'url']


class FilmSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    studios = StudioSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    cast = serializers.SerializerMethodField()
    crew = serializers.SerializerMethodField()

    streamings = serializers.SerializerMethodField()

    class Meta:
        model = Film
        fields = [
            'id', 'title', 'tagline', 'description',
            'release_date', 'duration',
            'poster', 'background', 'trailer_url',
            'genres', 'studios', 'tags',
            'streamings', 'cast', 'crew',
            'created_at', 'updated_at'
        ]

    def get_streamings(self, obj):
        items = FilmStreaming.objects.filter(film=obj)
        return FilmStreamingSerializer(items, many=True).data
    
    def get_cast(self, obj):
        roles = obj.film_roles.filter(role_type="ACTOR").select_related('artist').order_by('order')
        return [
            {
                "id": role.artist.id,
                "full_name": role.artist.full_name,
                "photo": role.artist.photo.url if role.artist.photo else None,
                "character_name": role.character_name
            }
            for role in roles
        ]

    def get_crew(self, obj):
        roles = obj.film_roles.exclude(role_type="ACTOR").select_related('artist')
        return [
            {
                "id": role.artist.id,
                "full_name": role.artist.full_name,
                "photo": role.artist.photo.url if role.artist.photo else None,
                "role": role.role_type
            }
            for role in roles
        ]

