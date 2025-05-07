import django_filters
from .models import Film

class FilmFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(field_name='genres__slug', lookup_expr='iexact')
    tag = django_filters.CharFilter(field_name='tags__slug', lookup_expr='iexact')
    studio = django_filters.CharFilter(field_name='studios__name', lookup_expr='iexact')
    year = django_filters.NumberFilter(field_name='release_date', lookup_expr='year')

    class Meta:
        model = Film
        fields = ['genre', 'tag', 'studio', 'year']
