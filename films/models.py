from django.db import models
from django.utils.text import slugify

class Genre(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Studio(models.Model):
    name = models.CharField(max_length=128)
    country = models.CharField(max_length=64, blank=True, null=True)
    founded_year = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Streaming(models.Model):
    name = models.CharField(max_length=128)
    logo = models.ImageField(upload_to='streaming_logos/', blank=True, null=True)

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Film(models.Model):
    title = models.CharField(max_length=200)
    tagline = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    release_date = models.DateField(blank=True, null=True)
    duration = models.PositiveIntegerField(help_text="Duration in minutes", blank=True, null=True)
    # Media fields
    poster = models.ImageField(upload_to='films/posters/', blank=True, null=True)
    background = models.ImageField(upload_to='films/backgrounds/', blank=True, null=True)
    trailer_url = models.URLField(blank=True, null=True)
    # Foreign fields
    genres = models.ManyToManyField(Genre, related_name='films')
    studios = models.ManyToManyField(Studio, related_name='films', blank=True)
    tags = models.ManyToManyField(Tag, related_name='films', blank=True)
    streamings = models.ManyToManyField(
        Streaming,
        through='FilmStreaming',
        related_name='films'
    )
    # Date fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class FilmStreaming(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    streaming = models.ForeignKey(Streaming, on_delete=models.CASCADE)
    url = models.URLField()

    class Meta:
        unique_together = ('film', 'streaming')

    def __str__(self):
        return f"{self.film.title} on {self.streaming.name}"