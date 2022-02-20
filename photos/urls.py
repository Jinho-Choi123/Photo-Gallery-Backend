from django.contrib import admin
from django.urls import path
from .views import GalleryView
import re 

urlpatterns = [
    path('<galleryId>/', GalleryView.as_view()),
    path('', GalleryView.as_view()),
]