from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('game_list')),
    #path("hworld/", include("hworld.urls")),
    path('admin/', admin.site.urls),
    path('games/', include('games.urls')),
]