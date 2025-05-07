from django.contrib import admin
from .models import FilmUserData, Review, ReviewLike, CustomList

admin.site.register(FilmUserData)
admin.site.register(Review)
admin.site.register(ReviewLike)
admin.site.register(CustomList)
