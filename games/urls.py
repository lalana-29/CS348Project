from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_list, name='game_list'),
    path('add/', views.game_add, name='game_add'),
    path('edit/<int:pk>/', views.game_edit, name='game_edit'),
    path('delete/<int:pk>/', views.game_delete, name='game_delete'),
]