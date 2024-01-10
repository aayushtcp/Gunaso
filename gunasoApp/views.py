from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.core.mail import send_mail
import re


from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.utils import timezone
from .models import UserPost,Profile, IndexProfile, Topic, TopicComment, Developer, Contact, Story, MyFeature
from django.contrib.auth.decorators import login_required
# from .models import Gunaso
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
from collections import defaultdict
from django.db.models import Count
# from .forms import UserProfileForm


def index(request):
    mainusers = IndexProfile.objects.all()[:4]
    
    alltopics = Topic.objects.all()
    context = {"username": request.user, "mainusers":mainusers, "alltopics":alltopics}
    return render(request, 'index.html',context)

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
        request.user.set_password(password)
        request.user.save()
        
        # Update profile picture
        if 'image' in request.FILES:
            userimageFU = request.FILES['image']
            profile.image = userimageFU
            profile.save()
            
        messages.success(request, 'Profile updated successfully.')
        return redirect('update_profile')
    return render(request,'update_profile.html', {'user': request.user})

    
@login_required(login_url='/login/')
def user_timeline(request, category):
    data = []
    date =[]
    finaldate_set = set()
    user_posts = UserPost.objects.filter(category=category)
    current_path = request.path
    path_parts = current_path.split('/')
    # Filter out empty parts
    path_parts = [part for part in path_parts if part]  
    # Get the last element (last word) if the path is not empty
    extracted_category = path_parts[-1] if path_parts else None
    print("The last word: ==" + extracted_category)
    
    date_count = defaultdict(int)

    for item in user_posts:
        data.append(item.category)
        date.append(item.created_at)
        
    # Remove Decimal objects by converting them to int
    actualdata = len(data)
    actualdate = [str(y) for y in date]
    
    for date_str in actualdate:
        # Convert string to datetime object
        try:
            date_object = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f%z')
        except ValueError:
            date_object = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S%z')
        # Get the formatted date with month name
        formatted_date = date_object.strftime('%d %B %Y %H:%M:%S %z')
        
        finaldate_set.add(formatted_date[3:6])
        date_count[formatted_date[3:6]] += 1 
        
    finaldate = list(finaldate_set)
    
    if request.user.username == extracted_category:
        if request.method == 'POST':
            # for feature image setup
            if 'file-input' in request.FILES:
                userimageFeature= request.FILES['file-input']
                feature = MyFeature(user = request.user, file = userimageFeature)
                feature.save()
                return redirect('user_timeline', category=extracted_category)
            return redirect('user_timeline', category=extracted_category)
    if request.method == 'POST':
        content = request.POST.get('content')
        hm = UserPost(user = request.user,category = extracted_category, content = content)
        hm.save()
        
        messages.success(request, 'Thought posted successfully.')
        return redirect('user_timeline', category=extracted_category)
    
    visited_user = User.objects.get(username=extracted_category)
    visited_user_profiles = Profile.objects.filter(user=visited_user)
    
    date_count_list = [date_count[date] for date in finaldate]
    
    #############################
    #####                  ######
    ## for user feature system ##
    #                           #
    myfeature = MyFeature.objects.filter(user = visited_user)
    
    uppercontext = {
        'user_posts': user_posts,   
        'extracted_category': extracted_category,
        'actualdata': actualdata,
        'finaldate': finaldate,
        'date_count_list':date_count_list,
        'visited_user_profiles': visited_user_profiles,
        'myfeature': myfeature
    }
    return render(request, 'user_timeline.html', uppercontext)


def famoustopics(request, slug):
    topic = Topic.objects.filter(slug=slug).first()
    comments = TopicComment.objects.filter(topic=topic)[::-1]
    context = {"topic": topic, "comments": comments}
    return render(request, 'famoustopics.html', context)


# Posting Thougths in Topic API
def postThoughts(request):
    if request.method == 'POST':
        comment =request.POST['comment']
        user =request.user
        postsno=request.POST['postsno']
        topic = Topic.objects.get(sno = postsno)
        # parent = request.POST['']
        
        comment = TopicComment(comment =comment, user=user,topic=topic)
        comment.save()
    return redirect(f'/topics/{topic.slug}')
                  
                  
def persons(request):
    allusers = Profile.objects.all() #[:4]
    context = {"allusers":allusers}
    return render(request, 'persons.html',context)

def topics(request):
    alltopics = Topic.objects.all()
    context = {"alltopics":alltopics}
    return render(request, 'topics.html', context) #edit this later

def developers(request):
    developers = Developer.objects.all()
    context = {"developers":developers}
    return render(request, 'developers.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        tosave = Contact(name = name, email = email, phone = phone, content = content)
        tosave.save()
        return render(request, 'contact.html')
    return render(request, 'contact.html')


def services(request):
    return render(request, 'services.html')

def gallary(request):
    return render(request, 'gallary.html')


def anonymity(request):
    return render(request, 'anonymity.html')

@login_required(login_url='/login/')
def writestory(request):
    if request.method == 'POST':
        user =request.user
        storySubject = request.POST['subject']
        storyType = request.POST['storytype']
        storyContent = request.POST['storycontent']
        saveStory = Story(user=user, storySubject= storySubject, storyType=storyType, storyContent=storyContent)
        saveStory.save()
        return redirect('/read-story')
    return render(request, 'writestory.html')

def readstory(request):
    stories = Story.objects.all()[::-1]
    context = {"stories":stories}
    return render(request, 'readstory.html', context)

@login_required(login_url='/login/')
def analytics(request):
    data = []
    date =[]
    finaldate_set = set()
    extracted_category  = request.user
    user_posts = UserPost.objects.filter(category=request.user)
    top_user_posts = UserPost.objects.values('category').annotate(post_count=Count('category')).order_by('-post_count')[:3]
    date_count = defaultdict(int)

    for item in user_posts:
        data.append(item.category)
        date.append(item.created_at)
        
    # Remove Decimal objects by converting them to int
    actualdata = len(data)
    actualdate = [str(y) for y in date]
    
    for date_str in actualdate:
        # Convert string to datetime object
        try:
            date_object = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f%z')
        except ValueError:
            date_object = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S%z')
        # Get the formatted date with month name
        formatted_date = date_object.strftime('%d %B %Y %H:%M:%S %z')
        
        finaldate_set.add(formatted_date[3:6])
        date_count[formatted_date[3:6]] += 1 
        
    finaldate = list(finaldate_set)
    date_count_list = [date_count[date] for date in finaldate]

    uppercontext = {
        'user_posts': user_posts,   
        'extracted_category': extracted_category,
        'actualdata': actualdata,
        'finaldate': finaldate,
        'date_count_list':date_count_list,
        'top_user_posts': top_user_posts
    }
    return render(request, 'analytics.html', uppercontext)

# to view the full story
def storyview(request, slug):
    fullstory  = Story.objects.filter(slug=slug).first()
    context = {"fullstory": fullstory}
    return render(request, 'storyview.html', context)

def yourstory(request):
    particularStory  = Story.objects.filter(user = request.user)
    context = {"particularStory":particularStory}
    return render(request, 'yourstory.html', context)


def deleteConfession(request, id):
    dele = UserPost.objects.filter(id=id)
    dele.delete()
    messages.success(request, "Deleted the post")
    return redirect('/')

def deleteFeature(request, id):
    dele = MyFeature.objects.filter(id=id)
    dele.delete()
    messages.success(request, "Deleted Featured Image")
    return redirect('/')

def privacypolicy(request):
    return render(request, 'privacypolicy.html')