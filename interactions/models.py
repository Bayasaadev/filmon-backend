from django.db import models
from django.contrib.auth.models import User
from films.models import Film


class FilmUserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='film_data')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='user_data')

    watched = models.BooleanField(default=False)
    liked = models.BooleanField(default=False)
    watchlisted = models.BooleanField(default=False)
    rating = models.FloatField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'film')

    def __str__(self):
        return f"{self.user.username} → {self.film.title}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    like_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('user', 'film')

    def __str__(self):
        return f"Review by {self.user.username} on {self.film.title}"
    
    
class ReviewLike(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'review')

    def __str__(self):
        return f"{self.user.username} liked review {self.review.id}"


class CustomList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_lists')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    films = models.ManyToManyField(Film, related_name='in_custom_lists')
    is_public = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return f"{self.user.username}'s list: {self.name}"
