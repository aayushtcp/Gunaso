from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.timezone import localtime, now
from django.utils.text import slugify

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
    
# class IndexTopic(models.Model):
#     name = models.OneToOneField(Topic, on_delete = models.CASCADE, related_name="majortopicfilter")
    
    
# For Topic Thoughts (Comments)
class TopicComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)
    
    def __str__(self):
        return self.comment[0:13] + ' ' + 'by -- ' + self.user.email
    
    
class Developer(models.Model):
    sno = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to="gunasoApp/images/developers", blank=True, default="upload-image-dev")
    name = models.CharField(max_length=30)
    position = models.CharField(max_length=30)
    bio = models.TextField()
    facebook = models.CharField(max_length=255)
    instagram = models.CharField(max_length=255)
    x = models.CharField(max_length=255)
    github = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name + " -- " + self.position
    
    
class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=55)
    email = models.CharField(max_length=90)
    phone = models.CharField(max_length=55)
    content = models.TextField()
    
    def __str__(self):
        return "Contact from -- " + self.name
    
    
class Story(models.Model):
    sno = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    storySubject = models.CharField(max_length = 255, blank=True)
    storyType = models.CharField(max_length = 50, blank=True)
    storyContent = models.TextField(blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.storySubject)
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Story By -- {self.user}"
    
    
class MyFeature(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "status")
    file = models.ImageField(upload_to="gunasoApp/images/featureImgs", blank=True, default="upload-image-feature")
    
    def __str__(self):
        return f'{self.user}\'s -  Feature'