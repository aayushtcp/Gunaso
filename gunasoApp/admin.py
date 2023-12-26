from django.contrib import admin
from .models import UserPost, Profile, IndexProfile
# Register your models here.

admin.site.register(UserPost)
admin.site.register(Profile)
admin.site.register(IndexProfile)