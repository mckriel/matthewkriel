from django.urls import path
from . import views

urlpatterns = [
    path('', views.pokedex_view, name='pokedex'),
]