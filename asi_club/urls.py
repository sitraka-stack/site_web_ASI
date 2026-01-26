"""
URL configuration for asi_club project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('club.urls')),  # Inclure les URLs de l'application club
]