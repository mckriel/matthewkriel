from django.urls import path
from .views import fitness_class_view

urlpatterns = [
    path('', fitness_class_view, name='pfa')
]