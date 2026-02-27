from django.urls import path

from .views import landing, privacy, support

urlpatterns = [
    path('', landing, name='countfree_landing'),
    path('privacy/', privacy, name='countfree_privacy'),
    path('support/', support, name='countfree_support'),
]
