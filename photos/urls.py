from django.contrib import admin
from django.urls import path
from .views import GalleryView, PhotoView
import re 

urlpatterns = [
    path('photo/', PhotoView.as_view()),
    path('<galleryId>/', GalleryView.as_view()),
    path('', GalleryView.as_view()),
]