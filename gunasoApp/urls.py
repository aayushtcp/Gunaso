"""testProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from gunasoApp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views

from django.contrib.auth.models import User
urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon/favicon.ico'))),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    
    # Login system urls
    path('signup/',views.handleSignup, name='signup'),
    path('login/',views.handleLogin, name='login'),
    path('logout/',views.handleLogout, name='logout'),
    
    # Update password whole system Url
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'), 
    
    
    path('user/<str:visitedUser>/', views.user_timeline, name='user_timeline'), #category is username from url
    path('analytics/', views.analytics, name='analytics'), #category is username from url for analytics
        
    # search systems
    path('searchperson/', views.searchperson, name="searchperson"),
    path('searchtopic/', views.searchtopic, name="searchtopic"),
    path('searchgroup/', views.searchgroup, name="searchgroup"),
    
    # person and topics list url
    path('persons/',views.persons, name='person'),
    path('topics/',views.topics, name='topics'),
    path('groups/',views.groups, name='groups'),
    
    path('developers/',views.developers, name='developers'),
    path('contact/',views.contact, name='contact'),
    # path('services/',views.services, name='services'),

    # gallary and anonymity (only forntend)
    path('gallary/',views.gallary, name='gallary'),
    path('anonymity/',views.anonymity, name='anonymity'),
    path('privacy-policy/',views.privacypolicy, name='privacypolicy'),

    # read and write story system with slugify
    path('write-story/',views.writestory, name='writestory'),
    path('read-story/<str:slug>',views.storyview, name='storyview'),
    path('read-story/',views.readstory, name='readstory'),
    path('yourstory/',views.yourstory, name='yourstory'),

    # for delete
    path('user/<str:visitedUser>/deleteConfession/<int:post_id>/', views.deleteConfession, name='delete_confession'),
    path('user/<str:visitedUser>/deleteFeature/<int:post_id>/', views.deleteFeature, name='deleteFeature'),
    
    # Update systems
    path('update_profile/',views.update_profile, name='update_profile'),
    path('update_intro/',views.editIntro, name='editIntro'),
    path('update-password/<str:user>/',views.update_password, name='updatePassword'),
    # path('change-password/<str:user>/',views.change_password, name='changePassword'),
    path('update-password/<str:user>/', views.update_password, name='update_password'),
    
    # celebraties/topics confessions/thoughts/comments
    path('postThoughts/',views.postThoughts, name='postThoughts'),
    path('postThoughtsGroup/',views.postThoughtsGroup, name='postThoughtsGroup'),
    
    # celebraties/topics particular slug
    path('topics/<str:slug>',views.famoustopics, name='famoustopics'),
    
    # for groups
        # create form of group
        path('create-group/',views.createGroup, name='createGroup'),
        # particular group slug system
        path('groups/<str:slug>',views.groupsparticular, name='groupsparticular'),
    
    # for clipping system user
    path('persons/<str:user>/clip-system/<str:visitedUser>/',views.clipping, name='clipping'),
    # for clipping system group
    path('groups/<str:user>/clip-system-group/<str:visitedGroup>/', views.groupClipping, name='groupClipping'),
    # for clipping system story
    path('read-story/<str:user>/clip-system-story/<str:visitedStory>/', views.storyClipping, name='storyClipping'),
    
    # for all unclip system------------------------------------------------------------------------------------------
    # unclip user
    path('persons/<str:user>/unclip-system/<str:visitedUser>/',views.unclipping, name='unclipping'),
    # unclip Group
    path('groups/<str:user>/unclip-group-system/<str:visitedGroup>/',views.group_unclipping, name='group_unclipping'),
    # unclip Story
    path('read-story/<str:user>/unclip-story-system/<str:visitedStory>/',views.story_unclipping, name='story_unclipping'),
    
    # to show clippings
    path('myclippings/', views.showClippings, name='showClippings'),
    path('save_webpush_info/', views.send_push_notification, name='save_webpush_info'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)