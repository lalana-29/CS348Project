from django.contrib import admin
from .models import Platform, Developer, Game, Review

admin.site.register(Platform)
admin.site.register(Developer)
admin.site.register(Game)
admin.site.register(Review)