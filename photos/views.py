from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import GallerySerializer
# Create your views here.

# Create Gallery
class GalleryCreate(APIView):
    def post(self, request):
        
        gallery_serializer = GallerySerializer(data=request.data, context = {'user': request.user.id})
        gallery_serializer.is_valid(raise_exception=True)
        gallery_serializer.create(request.data)
        return Response({"msg": "Gallery Created"}, status=status.HTTP_201_CREATED)

