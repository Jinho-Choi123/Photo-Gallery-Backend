from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Photo, Gallery
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

#handle photo upload
class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'image', 'uploaded_at', 'galleryId', 'size')
    
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
        #limit max size of photo to 25MB
        size = validated_data['image'].size
        if size > 25000000:
            raise serializers.ValidationError("Photo size is too large")

        photo = Photo.objects.create(
            image = validated_data['image'],
            galleryId = validated_data['galleryId'],
            size = size,
        )
        photo.save()
        return photo
    def delete(self, validated_data):
        photo = Photo.objects.get(id = validated_data['id'])
        photo.delete()
        return photo
    def move(self, validated_data):
        photo = Photo.objects.get(id = validated_data['id'])
        photo.galleryId = validated_data['galleryId']
        photo.save()
        return photo
    def copy(self, validated_data):
        photo = Photo.objects.get(id = validated_data['id'])
        new_photo = Photo.objects.create(
            image = photo.image,
            galleryId = validated_data['galleryId'],
            size = photo.size,
        )
        new_photo.save()
        return new_photo


class GallerySerializer(serializers.ModelSerializer):

    # New Gallery title must be unique
    title = serializers.CharField(
        required=True,
    )

    class Meta:
        model = Gallery
        fields = ('id', 'title', 'description', 'created_at')

    @staticmethod
    def check_ownership(userId, galleryId):
        if Gallery.objects.get(id = galleryId).user != User.objects.get(id = userId):
            raise serializers.ValidationError("You are not the owner of this gallery")
        return True
    
    def validate(self, data):
        return data

    def create(self, validated_data):
        #no duplicated gallery title for single user
        title = validated_data['title']
        user = User.objects.get(id = self.context['user'])
        if Gallery.objects.filter(title = title, user = user).exists():
            raise serializers.ValidationError("Gallery title already exists")
            
        user = User.objects.get(id = self.context['user'])
        gallery = Gallery.objects.create(
            title = validated_data['title'],
            description = validated_data['description'],
            user = user,
        )
        gallery.save()
        return gallery
    
    #update or delete
    def update(self, instance, data):
            
        galleryId = instance.id
        userId = self.context['user']
        self.check_ownership(userId, galleryId)

        #modify gallery title, description
        instance.title = data['title']
        instance.description = data['description']
        instance.save()
        return instance
