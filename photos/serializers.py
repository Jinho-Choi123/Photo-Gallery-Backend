from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Photo, Gallery
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

#handle photo upload
class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'image', 'uploaded_at', 'galleryId')
    
    def validate(self, data):
        galleryId = data['galleryId']
        #validate if galleryId is valid
        if Gallery.objects.filter(id=galleryId).exists() == False:
            raise serializers.ValidationError("Gallery does not exist")
        #validate request user is the owner of gallery
        userId = self.context['user']
        if Gallery.objects.get(id=galleryId).user != User.objects.get(id=userId):
            raise serializers.ValidationError("You are not the owner of this gallery")
        return data
    
    def create(self, validated_data):
        photo = Photo.objects.create(
            image = validated_data['image'],
            galleryId = validated_data['galleryId'],
        )
        photo.save()
        return photo

class GallerySerializer(serializers.ModelSerializer):

    # New Gallery title must be unique
    title = serializers.CharField(
        required=True,
        # validators = [UniqueValidator(queryset = Gallery.objects.filter(user = self.context['request'].user.id))]
    )

    class Meta:
        model = Gallery
        fields = ('id', 'title', 'description', 'created_at')
    
    def validate(self, data):
        return data

    def create(self, validated_data):
        user = User.objects.get(id = self.context['user'])
        gallery = Gallery.objects.create(
            title = validated_data['title'],
            description = validated_data['description'],
            user = user,
        )
        gallery.save()
        return gallery