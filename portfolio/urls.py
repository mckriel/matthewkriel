from django.urls import path
from .views import index, about, career, projects, contact

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('career/', career, name='career'),
    path('projects/', projects, name='projects'),
    path('contact/', contact, name='contact'),
]