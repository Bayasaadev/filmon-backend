from django.db import models
from films.models import Film

class Artist(models.Model):
    full_name = models.CharField(max_length=128)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=64, blank=True, null=True)
    photo = models.ImageField(upload_to='artists/photos/', blank=True, null=True)

    def __str__(self):
        return self.full_name


class FilmArtistRole(models.Model):
    ROLE_CHOICES = [
        ('ACTOR', 'Actor'),
        ('DIRECTOR', 'Director'),
        ('WRITER', 'Writer'),
        ('PRODUCER', 'Producer'),
        # Add more if needed
    ]

    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='film_roles')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='artist_roles')
    role_type = models.CharField(max_length=20, choices=ROLE_CHOICES)
    character_name = models.CharField(max_length=128, blank=True, null=True)
    order = models.PositiveIntegerField(blank=True, null=True, help_text="Sorting order for cast")

    class Meta:
        unique_together = ('film', 'artist', 'role_type')

    def __str__(self):
        return f"{self.artist.full_name} as {self.character_name or self.role_type} in {self.film.title}"
