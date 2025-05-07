from rest_framework import serializers
from .models import FilmUserData, Review, CustomList
from films.serializers import FilmSerializer
from django.contrib.auth.models import User


class FilmUserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilmUserData
        fields = [
            'id', 'film', 'watched', 'liked', 'watchlisted',
            'rating', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_avatar = serializers.SerializerMethodField()
    user_rating = serializers.SerializerMethodField()
    is_liked_by_me = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = [
            'id', 'film', 'username', 'user_avatar', 'user_rating',
            'content', 'like_count', 'is_liked_by_me',
            'created_at', 'updated_at'
        ]

    def get_user_avatar(self, obj):
        # Placeholder: add avatar logic when UserProfile is in place
        return None

    def get_user_rating(self, obj):
        user_data = FilmUserData.objects.filter(user=obj.user, film=obj.film).first()
        return user_data.rating if user_data else None

    def get_is_liked_by_me(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.likes.filter(user=user).exists()
        return False


class CustomListSerializer(serializers.ModelSerializer):
    films = FilmSerializer(many=True, read_only=True)

    class Meta:
        model = CustomList
        fields = ['id', 'name', 'description', 'films', 'is_public', 'created_at']
