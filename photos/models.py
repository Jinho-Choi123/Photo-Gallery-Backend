from djongo import models

class Gallery(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

class Photo(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='photos/%Y/%m/%d')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    galleryId = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name="photos")


