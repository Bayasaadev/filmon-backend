from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import FilmUserData, Review, ReviewLike, CustomList
from .serializers import FilmUserDataSerializer, ReviewSerializer, CustomListSerializer
from films.models import Film


class FilmUserDataViewSet(viewsets.ModelViewSet):
    queryset = FilmUserData.objects.all()
    serializer_class = FilmUserDataSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FilmUserData.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related('user', 'film')
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        film_id = self.request.query_params.get('film')
        qs = Review.objects.all()
        if film_id:
            qs = qs.filter(film_id=film_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def toggle_like(self, request, pk=None):
        review = self.get_object()
        user = request.user

        like, created = ReviewLike.objects.get_or_create(user=user, review=review)

        if not created:
            like.delete()
            review.like_count = review.likes.count()
            review.save()
            return Response({'detail': 'Unliked.'}, status=200)

        review.like_count = review.likes.count()
        review.save()
        return Response({'detail': 'Liked.'}, status=201)


class CustomListViewSet(viewsets.ModelViewSet):
    queryset = CustomList.objects.all()
    serializer_class = CustomListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CustomList.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_film(self, request, pk=None):
        custom_list = self.get_object()
        film_id = request.data.get('film_id')
        try:
            film = Film.objects.get(pk=film_id)
            custom_list.films.add(film)
            return Response({'detail': 'Film added.'})
        except Film.DoesNotExist:
            return Response({'detail': 'Film not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def remove_film(self, request, pk=None):
        custom_list = self.get_object()
        film_id = request.data.get('film_id')
        try:
            film = Film.objects.get(pk=film_id)
            custom_list.films.remove(film)
            return Response({'detail': 'Film removed.'})
        except Film.DoesNotExist:
            return Response({'detail': 'Film not found.'}, status=status.HTTP_404_NOT_FOUND)
