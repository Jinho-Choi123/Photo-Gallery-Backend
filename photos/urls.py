from django.contrib import admin
from django.urls import path
from .views import GalleryCreate

urlpatterns = [
    path('create/', GalleryCreate.as_view(), name='gallery_create'),
]