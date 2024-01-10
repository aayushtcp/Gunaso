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

from django.contrib.auth.models import User
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    # path('profile/<str:slug>/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile, name='user_profile'),
    # path('profile/', views.profile, name='profile'),
    # path('presignup/', views.prehandleSignup, name='presignup'),
    # path('prelogin/', views.prehandleLogin, name='prelogin'),
    # path('prelogin/', views.user_timeline, name='user_timeline'),
    
    # Login system urls
    path('signup/',views.handleSignup, name='signup'),
    path('login/',views.handleLogin, name='login'),
    
    path('user/<str:category>/', views.user_timeline, name='user_timeline'), #category is username from url
    path('analytics/', views.analytics, name='analytics'), #category is username from url for analytics
    
    path('logout/',views.handleLogout, name='logout'),
    
    path('persons/',views.persons, name='person'),
    path('topics/',views.topics, name='topics'),
    path('developers/',views.developers, name='developers'),
    path('contact/',views.contact, name='contact'),
    path('services/',views.services, name='services'),
    path('gallary/',views.gallary, name='gallary'),
    path('anonymity/',views.anonymity, name='anonymity'),
    path('write-story/',views.writestory, name='writestory'),
    path('read-story/<str:slug>',views.storyview, name='storyview'),
    path('read-story/',views.readstory, name='readstory'),
    path('yourstory/',views.yourstory, name='yourstory'),
    path('deleteConfession/<int:id>/', views.deleteConfession, name='deleteConfession'),
    
    path('update_profile/',views.update_profile, name='update_profile'),
    path('privacy-policy/',views.privacypolicy, name='privacypolicy'),
    
    path('postThoughts/',views.postThoughts, name='postThoughts'),
    
    path('topics/<str:slug>',views.famoustopics, name='famoustopics'),
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)