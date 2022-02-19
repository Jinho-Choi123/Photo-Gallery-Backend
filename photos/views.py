from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import GallerySerializer, PhotoSerializer
# Create your views here.

# Create Gallery
class GalleryCreate(APIView):
    def post(self, request):
        
        gallery_serializer = GallerySerializer(data=request.data, context = {'user': request.user.id})
        gallery_serializer.is_valid(raise_exception=True)
        gallery_serializer.create(request.data)
        return Response({"msg": "Gallery Created"}, status=status.HTTP_201_CREATED)

#Upload Single Photo
class PhotoUpload(APIView):
    def post(self, request):

        photo_serializer = PhotoSerializer(data=request.data, context = {'user': request.user.id})
        photo_serializer.is_valid(raise_exception=True)
        photo_serializer.create(request.data)
        return Response({"msg": "Photo Uploaded"}, status=status.HTTP_201_CREATED)"})