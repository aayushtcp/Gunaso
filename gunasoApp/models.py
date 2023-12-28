from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.timezone import localtime

# Create your models here.

class UserPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category  =models.CharField(max_length=30, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.created_at}'
    
    
    
# Models for profile picture of user

class Profile(models.Model):
    # user = models.CharField(max_length=55, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="Profile")
    image = models.ImageField(upload_to="gunasoApp/images", blank=True, default="upload-image")
    
    def __str__(self):
        # return f'{self.user.username} -  Profile'
        return f'{self.user} -  Profile'
    
    
class IndexProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="IndexProfile")
    image = models.ImageField(upload_to="gunasoApp/images/indexpost", blank=True, default="upload-image")
    
    def __str__(self):
        # return f'{self.user.username} -  Profile'
        return f'{self.user} -  IndexProfile'
    

class Topic(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    date = models.DateTimeField()
    tagone = models.CharField(max_length=10)
    tagtwo = models.CharField(max_length=10)
    slug = models.CharField(max_length=130, default="slugthis")
    image = models.ImageField(upload_to="gunasoApp/images/topicimages", blank=True, default="upload-image")
    introduction = models.TextField()
    
    def __str__(self):
        return f'Topic of -- {self.name} -'