from django.contrib import admin

from .models import Genre, Category, Titles, Review, Comments

admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Titles)
admin.site.register(Review)
admin.site.register(Comments)
