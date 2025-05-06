from django.contrib import admin
from .models import Film, Genre, Studio, Streaming, Tag

admin.site.register(Film)
admin.site.register(Genre)
admin.site.register(Studio)
admin.site.register(Streaming)
admin.site.register(Tag)
