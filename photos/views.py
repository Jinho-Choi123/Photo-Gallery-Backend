from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import GallerySerializer, PhotoSerializer
from .models import Gallery
# Create your views here.

# Create Gallery
class GalleryView(APIView):

    def get(self, request):
        galleries = Gallery.objects.filter(user = request.user.id)
        gallery_serializer = GallerySerializer(galleries, many=True)
        return Response(gallery_serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        gallery_serializer = GallerySerializer(data=request.data, context = {'user': request.user.id})
        gallery_serializer.is_valid(raise_exception=True)
        gallery_serializer.create(request.data)
        return Response({"msg": "Gallery Created"}, status=status.HTTP_201_CREATED)

    def delete(self, request, **kwargs):
        try:
            gallery = Gallery.objects.get(id = kwargs['galleryId'], user = request.user.id)
            gallery.delete()
        except Gallery.DoesNotExist:
            return Response({"error": "Gallery does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Unknown Error"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg": "Gallery Deleted"}, status=status.HTTP_200_OK)
        
    def put(self, request, **kwargs):
        gallery = Gallery.objects.get(id = kwargs['galleryId'], user = request.user.id)
        gallery_serializer = GallerySerializer(instance = gallery, data = request.data, context = {'user': request.user.id})
        gallery_serializer.is_valid(raise_exception=True)
        gallery_serializer.save()
        return Response({"msg": "Gallery Modified"}, status=status.HTTP_200_OK)



#Upload and get Photo
class Photo(APIView):
    def get(self, request):
        photo = Photo.objects.filter(galleryId = request.GET['galleryId'])
        photo_serializer = PhotoSerializer(photo, many=True)
        return Response(photo_serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        photo_serializer = PhotoSerializer(data=request.data, context = {'user': request.user.id}, many=True)
        photo_serializer.is_valid(raise_exception=True)
        photo_serializer.create(request.data)
        return Response({"msg": "Photo Uploaded"}, status=status.HTTP_201_CREATED)
    def delete(self, request):

        #check the ownership of the gallery
        if(not Gallery.objects.filter(id = request.data['galleryId'], user = request.user.id).exists()):
            return Response({"error": "Gallery does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            photos = Photo.objects.filter(id__in = request.data['id'], galleryId = request.data['galleryId'])
            photos.delete()
        except Photo.DoesNotExist:
            return Response({"error": "Photo does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Unknown Error"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg": "Photo Deleted"}, status=status.HTTP_200_OK)
