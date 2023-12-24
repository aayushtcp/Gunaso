from django.contrib.auth.models import User
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