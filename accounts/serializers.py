from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import UserProfile
from interactions.models import FilmUserData, Review, CustomList
from films.serializers import FilmSerializer
from films.models import Film

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)
    new_password2 = serializers.CharField(required=True)

    def validate(self, data):
        if data["new_password"] != data["new_password2"]:
            raise serializers.ValidationError("New passwords do not match.")
        return data
    
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        reset_link = f"http://localhost:3000/reset-password?uid={uid}&token={token}"
        send_mail(
            subject="Reset your Filmon password",
            message=f"Click the link to reset your password: {reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=6)

    def validate(self, data):
        try:
            uid = urlsafe_base64_decode(data["uid"]).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            raise serializers.ValidationError("Invalid UID.")

        if not default_token_generator.check_token(user, data["token"]):
            raise serializers.ValidationError("Invalid or expired token.")

        data["user"] = user
        return data

    def save(self):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["new_password"])
        user.save()


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    is_staff = serializers.BooleanField(source='user.is_staff', read_only=True)
    is_superuser = serializers.BooleanField(source='user.is_superuser', read_only=True)
    watched_count = serializers.SerializerMethodField()
    watchlisted_count = serializers.SerializerMethodField()
    liked_count = serializers.SerializerMethodField()
    recent_reviews = serializers.SerializerMethodField()
    recent_watched = serializers.SerializerMethodField()
    favorite_films = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'username', 'email', 'avatar', 'bio', 'location', 'website',
            'is_staff', 'is_superuser',
            'watched_count', 'watchlisted_count', 'liked_count',
            'recent_reviews', 'recent_watched', 'favorite_films'
        ]
        read_only_fields = [
            'username', 'email', 'is_staff', 'is_superuser',
            'watched_count', 'watchlisted_count', 'liked_count',
            'recent_reviews', 'recent_watched', 'favorite_films'
        ]
        extra_kwargs = {
            'avatar': {'required': False},
            'bio': {'required': False},
            'location': {'required': False},
            'website': {'required': False},
        }

    def get_avatar(self, obj):
        request = self.context.get('request')
        if obj.avatar and request:
            return request.build_absolute_uri(obj.avatar.url)
        return None

    def get_watched_count(self, obj):
        return FilmUserData.objects.filter(user=obj.user, watched=True).count()

    def get_watchlisted_count(self, obj):
        return FilmUserData.objects.filter(user=obj.user, watchlisted=True).count()

    def get_liked_count(self, obj):
        return FilmUserData.objects.filter(user=obj.user, liked=True).count()

    def get_recent_reviews(self, obj):
        reviews = Review.objects.filter(user=obj.user).select_related('film')[:5]
        return [{
            "film": review.film.title,
            "film_id": review.film.id,
            "content": review.content,
            "created_at": review.created_at
        } for review in reviews]

    def get_recent_watched(self, obj):
        watched = FilmUserData.objects.filter(user=obj.user, watched=True).order_by('-updated_at').select_related('film')[:5]
        return FilmSerializer([entry.film for entry in watched], many=True).data

    def get_favorite_films(self, obj):
        # Assumes there's a public CustomList called "Favorites"
        favorites = CustomList.objects.filter(user=obj.user, name__iexact='favorites').first()
        if not favorites:
            return []
        return FilmSerializer(favorites.films.all()[:5], many=True).data
    
    def update(self, instance, validated_data):
        instance.bio = validated_data.get("bio", instance.bio)
        instance.location = validated_data.get("location", instance.location)
        instance.website = validated_data.get("website", instance.website)
        if validated_data.get("avatar"):
            instance.avatar = validated_data["avatar"]
        instance.save()
        return instance