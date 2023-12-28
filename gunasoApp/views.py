from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
import re


from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.utils import timezone
from .models import UserPost,Profile, IndexProfile, Topic
from django.contrib.auth.decorators import login_required
# from .models import Gunaso
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.contrib.auth.forms import UserCreationForm
# from .forms import UserProfileForm


def index(request):
    mainusers = IndexProfile.objects.all()[:4]
    return render(request, 'index.html', {"username": request.user, "mainusers":mainusers})    

def about(request):
    return render(request, 'about.html')


def prehandleSignup(request):
    return render(request, 'signup.html')

def prehandleLogin(request):
    return render(request, 'login.html')




# Signup
def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        cpassword = request.POST['cpassword']
        # for profile images
        userimage = request.FILES['image']
    
        # check/verify
        if(password != cpassword):
            messages.error(request, "Password mismatch")
            return redirect("/")
        
        if(len(username) >10):
            messages.warning(request, "Username is greater than 10 characters")
            return redirect("/")

        # Create a new user
        myuser = User.objects.create_user(username, email, password)
        myuser.save()
        
        # !login directly user starts
        user = authenticate(username= username, password= password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            # profile pic upload to Profile modal DB
            profile = Profile(user=request.user, image=userimage)
            profile.save()
            return redirect("/")
        else:
            messages.error(request, "Username or password incorrect")
            return redirect("/")
        # return redirect("/")
        return render(request, 'login.html')
        # !login directly user ends

        messages.success(request, "User created sucessfully!")
        print(f"Hello {username}")
        return redirect('/')
    else:
        HttpResponse("Hiro na ban")
    return render(request,'signup.html')

# Login
def handleLogin(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        
        user = authenticate(username= loginusername, password= loginpassword)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect("/")
        else:
            messages.error(request, "Username or password incorrect")
            return redirect("/")
    # return redirect("/")
    return render(request, 'login.html')

def handleLogout(request):
    logout(request)
    messages.success(request, "Logout successful")
    return redirect("/")


def profile(request):
    return render(request,'profile.html')

@login_required(login_url='/login/')
def update_profile(request):
    '''to update user profile'''
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        userimageFU = request.FILES['image']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        
        # check/verify
        if(password != cpassword):
            messages.error(request, "Password mismatch")
            return redirect("update_profile")
        
        if(len(username) >10):
            messages.warning(request, "Username is greater than 10 characters")
            return redirect("update_profile")
        
        # Update user profile
        request.user.username = username
        request.user.email = email
        request.user.email = password
        request.user.save()
        
        # Update profile picture
        if userimageFU:
            profile.image = userimageFU
            profile.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('update_profile')
    return render(request,'update_profile.html', {'user': request.user})

    
@login_required(login_url='/login/')
def user_timeline(request, category):
    # print(f"The id is: ====={request.user.id}")
    user_posts = UserPost.objects.filter(category=category)
    # forimgfetch = Profile.objects.filter(user=category)
    # res = str(request.user)
    current_path = request.path
    
    path_parts = current_path.split('/')
    
    # Filter out empty parts
    path_parts = [part for part in path_parts if part]
    
    # Get the last element (last word) if the path is not empty
    extracted_category = path_parts[-1] if path_parts else None
    print("The last word: ==" + extracted_category)

    
    if request.method == 'POST':
        content = request.POST.get('content')
        # UserPost.objects.create(user=request.user, content=content, created_at=timezone.now())
        # hm = UserPost(user = request.user, content = content)
        hm = UserPost(user = request.user,category = extracted_category, content = content)
        hm.save()
        return redirect('user_timeline', category=extracted_category)
    return render(request, 'user_timeline.html', {'user_posts': user_posts, 'extracted_category': extracted_category})


def famoustopics(request, slug):
    post = Topic.objects.filter(slug=slug).first()
    context = {"post": post}
    return render(request, 'famoustopics.html', context)