from django.contrib import admin
from .models import UserPost, Profile, IndexProfile, Topic, TopicComment, Developer, Contact, Story, MyFeature, ConfessGroup, GroupsComments,Clipping,Groupclipping,Storyclipping
# Register your models here.

admin.site.register(UserPost)
admin.site.register(Profile)
admin.site.register(IndexProfile)
admin.site.register(Topic)
admin.site.register(TopicComment)
admin.site.register(Developer)
admin.site.register(Contact)
admin.site.register(Story)
admin.site.register(MyFeature)
admin.site.register(ConfessGroup)
admin.site.register(GroupsComments)
admin.site.register(Clipping)
admin.site.register(Groupclipping)
admin.site.register(Storyclipping)