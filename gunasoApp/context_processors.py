from .models import UserPost,Profile

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
def custom_context(request,category):
    if request.user.is_authenticated:
        user_posts = UserPost.objects.filter(category=category)
        forimgfetch = Profile.objects.filter(user=category)
        # res = str(request.user)
        current_path = request.path

        path_parts = current_path.split('/')
    
        # Filter out empty parts
        path_parts = [part for part in path_parts if part]
    
        # Get the last element (last word) if the path is not empty
        extracted_category = path_parts[-1] if path_parts else None
        print("The last word: ==" + extracted_category)

        return redirect('user_timeline', category=extracted_category)
    else:
        user_profile = None
    return render(request, 'user_timeline.html', {'user_posts': user_posts, 'extracted_category': extracted_category, 'forimgfetch':forimgfetch})