from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseForbidden,HttpResponseNotFound,HttpResponseBadRequest,HttpResponseRedirect
from django.core.mail import send_mail
import re
from gunasoApp.templatetags import extras,filters
from webpush import send_user_notification

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.utils import timezone
from .models import UserPost,Profile, IndexProfile, Topic, TopicComment, Developer, Contact, Story, MyFeature,ConfessGroup,GroupsComments,Clipping,Groupclipping,Storyclipping
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
from collections import defaultdict
from django.db.models import Count
from django.urls import resolve

# esewa
# Hash secret  key esewa integration V2
import uuid
import hmac
import hashlib
import base64

# to prevent nude and unusual images
from nudenet import NudeDetector

# custom 404 view
def not_found(request,exception):
    return render(request, '404.html')

def index(request):
    # mainusers = IndexProfile.objects.all()[:8]
    mainusers = Profile.objects.all()[:4]
    
    alltopics = Topic.objects.all()
    context = {"username": request.user, "mainusers":mainusers, "alltopics":alltopics}
    return render(request, 'indexbackup.html',context)

def about(request):
    user = request.user 
    
    if request.method == 'POST':
        amtt = request.POST['paisa']
        res = int(amtt)
        def genSha256(key, message):
            key = key.encode('utf-8')
            message = message.encode('utf-8')

            hmac_sha256 = hmac.new(key, message, hashlib.sha256)
            digest = hmac_sha256.digest()

            # Convert the digest to a Base64-encoded string
            signature = base64.b64encode(digest).decode('utf-8')

            return signature

        # total_amount = res
        total_amount = res
        secret_key = "8gBm/:&EnhH.1/q"
        uid= uuid.uuid4()
        data_to_sign = f"total_amount={total_amount},transaction_uuid={uid},product_code=EPAYTEST"

        result = genSha256(secret_key, data_to_sign)
        
        # to save in DB
        user = user
        #! transaction = Transaction(user = user, amount=amtt, unit_khapat=unit_khapat)
        # transaction.save()
        context = {
                'amtt': amtt,
                "res":res,
                'total_amount': total_amount,
                'uid': uid,
                'signature': result
        }
        return render(request, "foresewa.html", context)
    return render(request, 'about.html')


# def prehandleSignup(request):
#     return render(request, 'signup.html')

# def prehandleLogin(request):
#     return render(request, 'login.html')




# Signup
def handleSignup(request):
    if request.method == 'POST':
        first_name = request.POST['intro'].strip()
        username = request.POST['username'].strip()
        password = request.POST['password'].strip()
        email = request.POST['email'].strip()
        cpassword = request.POST['cpassword'].strip()
        # for profile images
        userimage = request.FILES['image']
    

        # ------------------------for nuditity------------------------------------------------------------
        # Use NudeNet to detect nudity
        detector = NudeDetector()
        
        # Save the uploaded image to a temporary file
        with open('temp_image.jpg', 'wb') as temp_image:
            for chunk in userimage.chunks():
                temp_image.write(chunk)
        # Use the detector to scan the temporary file
        result = detector.detect('temp_image.jpg')
        if result and 'score' in result[0]:
            score = result[0]['score']
            if (score > 0.75):
                imageclass = result[0]['class']
                if imageclass not in [
                    "FEMALE_GENITALIA_COVERED",
                    "FACE_FEMALE",
                    "FEET_EXPOSED",
                    "BELLY_COVERED",
                    "FEET_COVERED",
                    "ARMPITS_COVERED",
                    "FACE_MALE",
                    "MALE_GENITALIA_EXPOSED",
                    "ANUS_COVERED",
                    "FEMALE_BREAST_COVERED",
                    "BUTTOCKS_COVERED"
                    ]:
                    messages.error(request, "Sorry, the uploaded image contains explicit content.")
                    return redirect("/signup")
                
        if not (first_name or username or password or email or cpassword):
            messages.error(request, "Sorry, the uploaded image contains explicit content.")
            return redirect("/signup")

        elif password != cpassword:
            messages.error(request, "Password mismatch")
            return redirect("/signup")

        elif len(username) > 15:
            messages.warning(request, "Username is greater than 15 characters")
            return redirect("/signup")

        # Create a new user
        if(User.objects.filter(username = username)):
            messages.error(request, "Username already exists")
            return redirect('/signup')
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = first_name  #first name is for intro(bio)
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
            return redirect("/login")
    else:
        HttpResponse("Hiro na ban")
    return render(request,'signup.html')

# Login
def handleLogin(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        finalusername = loginusername.strip()
        finalpass = loginpassword.strip()
        user = authenticate(username= finalusername, password= finalpass)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect("/")
        else:
            messages.error(request, "Username or password incorrect")
            return redirect("/login")
    return render(request, 'login.html')

def handleLogout(request):
    logout(request)
    messages.success(request, "Logout successful")
    return redirect("/")

@login_required(login_url='/login/')
def update_profile(request):
    '''to update user profile'''
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        username = request.POST['username'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password'].strip()
        cpassword = request.POST['cpassword'].strip()
        
        # check/verify
        if(password != cpassword):
            messages.error(request, "Your confirm password is not matching")
            return redirect("update_profile")
        
        if(len(username) >10):
            messages.warning(request, "Username is greater than 10 characters")
            return redirect("update_profile")
        # check the existing user
        if(User.objects.filter(username = username)):
            messages.error(request, "Username already in use")
            return redirect('/update_profile')
        
        # username validation
        if(username):
            username_regex = re.compile(r'^[a-zA-Z][a-zA-Z0-9]*$')
            if not username_regex.match(username):
                messages.error(request,"Invalid username")
                return redirect('/update_profile')
        elif(email):
            email_regix = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
            if not email_regix.match(email):
                messages.error(request,"Invalid email")
                return redirect('/update_profile')
        elif(password):
            password_regex = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,32}$')
            if not password_regex.match(password):
                messages.error(request,"Invalid password")
                return redirect('/update_profile')
            
        
        # Update user profile
        if (username):
            request.user.username = username
        if (email):
            request.user.email = email
        if (password):
            request.user.set_password(password)
            
        request.user.save()
        
        # Update profile picture
        if 'image' in request.FILES:
            userimageFU = request.FILES['image']
            # ------------------------for nuditity------------------------------------------------------------
            # Use NudeNet to detect nudity
            detector = NudeDetector()
            
            # Save the uploaded image to a temporary file
            with open('temp_image.jpg', 'wb') as temp_image:
                for chunk in userimageFU.chunks():
                    temp_image.write(chunk)
            # Use the detector to scan the temporary file
            result = detector.detect('temp_image.jpg')
            if result and 'score' in result[0]:
                score = result[0]['score']
                if (score > 0.75):
                    imageclass = result[0]['class']
                    if (imageclass == "FACE_FEMALE" and score > 0.87):
                        messages.error(request, "Sorry, the uploaded image contains explicit content.")
                        return redirect("update_profile")
                    if imageclass not in [
                        "FEMALE_GENITALIA_COVERED",
                        "FACE_FEMALE",
                        "FEET_EXPOSED",
                        "BELLY_COVERED",
                        "FEET_COVERED",
                        "ARMPITS_COVERED",
                        "FACE_MALE",
                        "MALE_GENITALIA_EXPOSED",
                        "ANUS_COVERED",
                        "FEMALE_BREAST_COVERED",
                        "BUTTOCKS_COVERED"
                        ]:
                        messages.error(request, "Sorry, the uploaded image contains explicit content.")
                        return redirect("update_profile")

            # ------------------------------------------------------------------------------------------------
            profile.image = userimageFU
            profile.save()
            
        messages.success(request, 'Profile updated successfully.')
        return redirect('update_profile')
    return render(request,'update_profile.html', {'user': request.user})

    
@login_required(login_url='/login/')
def user_timeline(request, visitedUser):
    data = []
    date =[]
    finaldate_set = set()
    visited_user = get_object_or_404(User, username=visitedUser)
    user_posts = UserPost.objects.filter(visitedUser=visited_user)

    current_path = request.path
    path_parts = current_path.split('/')
    # Filter out empty parts
    path_parts = [part for part in path_parts if part]  
    # Get the last element (last word) if the path is not empty
    extracted_category = path_parts[-1] if path_parts else None
    print("The last word: == " + extracted_category)
    
    date_count = defaultdict(int)

    for item in user_posts:
        data.append(item.visitedUser)
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
            userimageFeature= request.FILES['file-input']
            # for feature image setup
            if 'file-input' in request.FILES:
                # ------------------------for nuditity------------------------------------------------------------
                # Use NudeNet to detect nudity
                detector = NudeDetector()
                
                # Save the uploaded image to a temporary file
                with open('temp_image.jpg', 'wb') as temp_image:
                    for chunk in userimageFeature.chunks():
                        temp_image.write(chunk)
                # Use the detector to scan the temporary file
                result = detector.detect('temp_image.jpg')
                if result and 'score' in result[0]:
                    score = result[0]['score']
                    print(f"Nudity score: {score}")
                    if (score > 0.75):
                        imageclass = result[0]['class']
                        print(f"Class: {imageclass}")
                        if (imageclass == "FACE_FEMALE" and score > 0.87):
                            print("Removing face female....")
                            messages.error(request, "Sorry, the uploaded image contains explicit content.")
                            return redirect("user_timeline", visitedUser=extracted_category)
                        if imageclass not in [
                            "FEMALE_GENITALIA_COVERED",
                            "FACE_FEMALE",
                            "FEET_EXPOSED",
                            "BELLY_COVERED",
                            "FEET_COVERED",
                            "ARMPITS_COVERED",
                            "FACE_MALE",
                            "MALE_GENITALIA_EXPOSED",
                            "ANUS_COVERED",
                            "FEMALE_BREAST_COVERED",
                            "BUTTOCKS_COVERED"
                            ]:
                            print("Removing....")
                            messages.error(request, "Sorry, the uploaded image contains explicit content.")
                            return redirect("user_timeline", visitedUser=extracted_category)
                # ------------------------------------------------------------------------------------------------
                feature = MyFeature(user = request.user, file = userimageFeature)
                feature.save()
                return redirect('user_timeline', visitedUser=extracted_category)
            return redirect('user_timeline', visitedUser=extracted_category)
    if request.method == 'POST':
        content = request.POST.get('content')
        hm = UserPost(user=request.user, visitedUser=visited_user, content=content)
        hm.save()
        messages.success(request, 'Thought posted successfully.')
        return redirect('user_timeline', visitedUser=visited_user)
        
    
    visited_user = User.objects.get(username=extracted_category)
    visited_user_profiles = Profile.objects.filter(user=visited_user)

    date_count_list = [date_count[date] for date in finaldate]

    # For user Feature System (Image)
    myfeature = MyFeature.objects.filter(user = visited_user)
    myintro = User.objects.filter(username = visited_user)
    
    uppercontext = {
        'user_posts': user_posts,   
        'extracted_category': extracted_category,
        'actualdata': actualdata,
        'finaldate': finaldate,
        'date_count_list':date_count_list,
        'visited_user_profiles': visited_user_profiles,
        'myfeature': myfeature,
        'myintro': myintro
    }
    return render(request, 'user_timeline.html', uppercontext)

@login_required(login_url='/login/')
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
                  
def postThoughtsGroup(request):
    if request.method == 'POST':
        comment_text  = request.POST['comment']
        user = request.user
        postsno = request.POST.get('postsno')
        confessgroup = ConfessGroup.objects.get(sno=postsno)
        parentsno = request.POST['parentsno']

        if parentsno == "":
            comment = GroupsComments(comment=comment_text, user=user, topic=confessgroup)
            comment.save()
            # messages.success(request,"Confession has been added successfully")
            
            # Check for '@' and print words
            if '@' in comment_text:
                mentioned_words = [word for word in comment_text.split() if word.startswith('@')]
                print("Mentioned words1:", mentioned_words)
                for userfornotify in mentioned_words:
                    actual_username = userfornotify[1:]
                    print(f"{actual_username}")
                try:
                    user_to_notify = User.objects.get(username=actual_username)
                    payload = {"head": f"Mentioned in {confessgroup}!", "body": "You are Mentioned!",  "icon": "../static/images/logos/g-favicon-color.png"}
                    send_user_notification(user=user_to_notify, payload=payload, ttl=1000)
                    print("Mentioned userfornotify runned successfully....")
                except User.DoesNotExist:
                    print(f"User with username {actual_username} does not exist.")

        else:
            parent = GroupsComments.objects.get(sno=parentsno)
            comment = GroupsComments(comment=comment_text, user=user, topic=confessgroup, parent=parent)
            comment.save()
            # messages.success(request,"Reply has been added successfully")
            # Check for '@' and print words
            if '@' in comment_text:
                mentioned_words = [word for word in comment_text.split() if word.startswith('@')]
                print("Mentioned words:", mentioned_words)

    return redirect(f'/groups/{confessgroup.slug}')

           
# @login_required(login_url='/login/')             
def persons(request):
    if request.user.is_anonymous:
        all_users = Profile.objects.all()
        uppercontext = {
            "all_users": all_users,
        }
        return render(request, 'persons.html', uppercontext)
    else:
        clipped_users_fetch = Clipping.objects.filter(user=request.user)
        all_users = Profile.objects.all()
        saved_users = clipped_users_fetch.values_list('visitedUser', flat=True)
        context = {
            "all_users": all_users,
            "saved_users": saved_users,
        }
        return render(request, 'persons.html', context)
    

def topics(request):
    alltopics = Topic.objects.all()
    context = {"alltopics":alltopics}
    return render(request, 'topics.html', context) #edit this later

@login_required(login_url='/login/')
def createGroup(request):
    '''Create a new group form'''
    if request.method == 'POST':
        groupimg= request.FILES['groupimg']
        groupname = request.POST['groupName']
        groupintro = request.POST['groupIntro']
            # for feature image setup
        if 'groupimg' in request.FILES:
            # ------------------------for nuditity------------------------------------------------------------
            # Use NudeNet to detect nudity
            detector = NudeDetector()
            
            # Save the uploaded image to a temporary file
            with open('temp_image.jpg', 'wb') as temp_image:
                for chunk in groupimg.chunks():
                    temp_image.write(chunk)
            # Use the detector to scan the temporary file
            result = detector.detect('temp_image.jpg')
            if result and 'score' in result[0]:
                score = result[0]['score']
                print(f"Nudity score: {score}")
                if (score > 0.75):
                    imageclass = result[0]['class']
                    print(f"Class: {imageclass}")
                    if (imageclass == "FACE_FEMALE" and score > 0.87):
                        print("Removing face female....")
                        messages.error(request, "Sorry, the uploaded image contains explicit content.")
                        return redirect("user_timeline")
                    if imageclass not in [
                        "FEMALE_GENITALIA_COVERED",
                        "FACE_FEMALE",
                        "FEET_EXPOSED",
                        "BELLY_COVERED",
                        "FEET_COVERED",
                        "ARMPITS_COVERED",
                        "FACE_MALE",
                        "MALE_GENITALIA_EXPOSED",
                        "ANUS_COVERED",
                        "FEMALE_BREAST_COVERED",
                        "BUTTOCKS_COVERED"
                        ]:
                        print("Removing....")
                        messages.error(request, "Sorry, the uploaded image contains explicit content.")
                        return redirect("createGroup")
            # ------------------------------------------------------------------------------------------------
            newgroup = ConfessGroup(Groupname=groupname,owner = request.user, image = groupimg,introduction = groupintro)
            newgroup.save()
            messages.success(request, "Your Group is Created Successfully.")
            return redirect('groups')
        # return redirect('createGroup')
    return render(request, 'createGroup.html',{})

def groups(request):
    if request.user.is_anonymous:
        allgroups = ConfessGroup.objects.all()
        context = {"allgroups":allgroups}
        return render(request, 'groups.html', context)
    else:
        clippedGroups_fetch = Groupclipping.objects.filter(user=request.user)
        savedGroups = clippedGroups_fetch.values_list('visitedGroup', flat=True)
        allgroups = ConfessGroup.objects.all()
        context = {"allgroups":allgroups,"savedGroups":savedGroups}
        return render(request, 'groups.html', context)

@login_required(login_url='/login/')
def groupsparticular(request, slug):
    users = User.objects.all()
    allgroups = ConfessGroup.objects.filter(slug=slug).first()
    comments = GroupsComments.objects.filter(topic=allgroups, parent=None)[::-1]
    replies = GroupsComments.objects.filter(topic=allgroups).exclude(parent = None)
    # print(comments, replies)
    reply_dict={}
    for reply in replies:
        if reply.parent.sno not in reply_dict.keys():
            reply_dict[reply.parent.sno]= [reply]
        else:
            reply_dict[reply.parent.sno].append(reply)
            
    print(reply_dict)
    context = {"allgroups": allgroups, "comments": comments, "reply_dict": reply_dict, 'users': users}
    return render(request, 'groupParticular.html', context)

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
    if request.user.is_anonymous:
        stories = Story.objects.all()[::-1]
        context = {"stories":stories}
        return render(request, 'readstory.html', context)
    else:
        clippedStory_fetch = Storyclipping.objects.filter(user =request.user)
        saved_story = clippedStory_fetch.values_list('visitedStory', flat=True)
        stories = Story.objects.all()[::-1]
        # print(saved_story)
        context = {"stories":stories, 'saved_story':saved_story}
        return render(request, 'readstory.html', context)

@login_required(login_url='/login/')
def analytics(request):
    data = []
    date = []
    finaldate_set = set()
    extracted_category = request.user
    user_posts = UserPost.objects.filter(visitedUser=request.user)
    
    top_user_posts = UserPost.objects.values('visitedUser__username').annotate(post_count=Count('visitedUser')).order_by('-post_count')[:5]
    date_count = defaultdict(int)

    for item in user_posts:
        data.append(item.visitedUser.username)
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
        'date_count_list': date_count_list,
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

@login_required(login_url='/login/')
def deleteConfession(request,visitedUser,post_id):
    current_path = request.path
    path_parts = current_path.split('/')
    path_parts = [part for part in path_parts if part]
    
    extracted_category = path_parts[-3] if path_parts else None
                
    # Get the specific post by post_id
    try:
        post = UserPost.objects.get(id=post_id)
    except UserPost.DoesNotExist:
        return HttpResponseNotFound("Post not found.")
    # Check if the logged-in user is the owner of the post
    if request.user.username != extracted_category:
        return HttpResponseForbidden("Hiro na ban")
    else:
        # Only proceed with deletion if the user is the owner
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect(f"../../")

def deleteFeature(request,visitedUser,post_id):
    current_path = request.path
    path_parts = current_path.split('/')
    path_parts = [part for part in path_parts if part]
    
    extracted_category = path_parts[-3] if path_parts else None
            
    # Get the specific post by post_id
    try:
        post = MyFeature.objects.get(id=post_id)
    except UserPost.DoesNotExist:
        return HttpResponseNotFound("Post not found.")
    # Check if the logged-in user is the owner of the post
    if request.user.username != extracted_category:
        return HttpResponseForbidden("Hiro na ban randi ko ban.")
    else:
        # Only proceed with deletion if the user is the owner
        post.delete()
        messages.success(request, "Deleted the featured post")
        return redirect(f'../../../../user/{request.user.username}')


def privacypolicy(request):
    return render(request, 'privacypolicy.html')

# edit intro code
@login_required(login_url='/login/')
def editIntro(request):
    if request.method == 'POST':
        newintro = request.POST['newintro'].strip()
        request.user.first_name = newintro
        request.user.save()
        messages.success(request, "Intro Updated Successfully!")
        return redirect(f'../../../../user/{request.user.username}')
    else:
        return HttpResponseNotFound("HaHa Don't Try To Be Cool")
        
        
# Search for perosns
def searchperson(request):
    query = request.GET.get('query', '')

    if len(query) > 100:
        allPerson = Profile.objects.none()
    else:
        try:
            user_id = int(query)
            person = Profile.objects.filter(user_id=user_id)
        except ValueError:
            person = Profile.objects.none()
        
        if request.user.is_anonymous:
            allPersonContent = Profile.objects.filter(user__username__icontains=query)
            allPerson = person.union(allPersonContent)
            params = {'allPerson': allPerson, 'query': query}
        else:
            clipped_users_fetch = Clipping.objects.filter(user=request.user)
            saved_users = clipped_users_fetch.values_list('visitedUser', flat=True)
            allPersonContent = Profile.objects.filter(user__username__icontains=query)
            allPerson = person.union(allPersonContent)
            params = {'allPerson': allPerson, 'query': query, 'saved_users':saved_users}
    return render(request, 'searchperson.html', params)


# Search for topics
def searchtopic(request):
    query = request.GET.get('query', '')

    if len(query) > 100:
        allTopic = Topic.objects.none()
    else:
        try:
            user_id = int(query)
            topic = Topic.objects.filter(user_id=user_id)
        except ValueError:
            topic = Topic.objects.none()
        allTopicContent = Topic.objects.filter(name__icontains=query)
        allTopic = topic.union(allTopicContent)
    params = {'allTopic': allTopic, 'query': query}
    return render(request, 'topicsearch.html', params)


# Search for groups
def searchgroup(request):
    query = request.GET.get('query', '')

    if len(query) > 100:
        allGroup = ConfessGroup.objects.none()
    else:
        try:
            user_id = int(query)
            group = ConfessGroup.objects.filter(user_id=user_id)
        except ValueError:
            group = ConfessGroup.objects.none()
            
        if request.user.is_anonymous:
            allGroupContent = ConfessGroup.objects.filter(Groupname__icontains=query)
            allGroup = group.union(allGroupContent)
            params = {'allGroup': allGroup, 'query': query}
        else:
            clippedGroups_fetch = Groupclipping.objects.filter(user=request.user)
            savedGroups = clippedGroups_fetch.values_list('visitedGroup', flat=True)
            allGroupContent = ConfessGroup.objects.filter(Groupname__icontains=query)
            allGroup = group.union(allGroupContent)
            params = {'allGroup': allGroup, 'query': query, 'savedGroups':savedGroups}
    return render(request, 'groupsearch.html', params)


@login_required(login_url='/login/')
def clipping(request, *args, **kwargs):
    '''User clipping user or topic or group SYSTEM '''
    if request.method == 'POST':
        user = request.user
        visited_username = request.POST['visitedUser']
        visited_user = get_object_or_404(User, username=visited_username)
        saveClipping = Clipping(user=user, visitedUser=visited_user)
        saveClipping.save()
        # for push notification start---------------------------------+
        payload = {"head": "Clipping!", "body": "User Clipped Successfully", "icon": "../static/images/logos/g-favicon-color.png"}
        send_user_notification(user=user, payload=payload, ttl=1000)
        # ------------------------------------------------------------+
        messages.success(request, "Clipped Successfully")
        return redirect('/myclippings')
    else:
        return HttpResponseNotFound("HaHa Don't Try To Be Cool")
    
@login_required(login_url='/login/')
def unclipping(request, visitedUser, *args, **kwargs):
    '''User Un-clipping user SYSTEM '''
    if request.method == 'POST':
        current_user = request.user
        clipping_to_delete = get_object_or_404(Clipping, user=current_user, visitedUser__username=visitedUser)
        # Delete the clipping
        clipping_to_delete.delete()
        return redirect('/persons')
    else:
        return HttpResponseNotFound("HaHa Don't Try To Be Cool") 

@login_required(login_url='/login/')
def groupClipping(request, *args, **kwargs):
    '''User Group clipping user or topic or group SYSTEM '''
    if request.method == 'POST':
        user = request.user
        visited_group_name = request.POST['visitedGroup']
        visited_group = get_object_or_404(ConfessGroup, slug=visited_group_name)
        saveClipping = Groupclipping(user=user, visitedGroup=visited_group)
        saveClipping.save()

        messages.success(request, "Group Clipped Successfully")
        return redirect('/myclippings')
    else:
        message_error = "Are you trying to edit URL manually?" 
        return render(request,'404.html',{'message_error':message_error})
    
@login_required(login_url='/login/')
def group_unclipping(request, visitedGroup, *args, **kwargs):
    '''Group Un-clipping user SYSTEM '''
    if request.method == 'POST':
        current_user = request.user
        clipping_to_delete_group = get_object_or_404(Groupclipping, user=current_user, visitedGroup__slug=visitedGroup)
        # Delete the group clipping
        clipping_to_delete_group.delete()
        return redirect('/groups')
    else:
        return HttpResponseNotFound("HaHa Don't Try To Be Cool") 

@login_required(login_url='/login/')
def storyClipping(request, *args, **kwargs):
    '''User Story clipping SYSTEM '''
    if request.method == 'POST':
        user = request.user
        visited_story_name = request.POST['visitedStory']
        visited_story = get_object_or_404(Story, slug=visited_story_name)
        saveClipping = Storyclipping(user=user, visitedStory=visited_story)
        # print(saveClipping)
        saveClipping.save()

        messages.success(request, "Story Clipped Successfully")
        return redirect('/myclippings')
    else:
        return HttpResponseNotFound("HaHa Don't Try To Be Cool")
    
    
@login_required(login_url='/login/')
def story_unclipping(request, visitedStory, *args, **kwargs):
    '''Story Un-clipping user SYSTEM '''
    if request.method == 'POST':
        current_user = request.user
        clipping_to_delete_story = get_object_or_404(Storyclipping, user=current_user, visitedStory__slug=visitedStory)
        # Delete the story clipping
        clipping_to_delete_story.delete()
        messages.success(request,"Story Unclipped Successfully")
        return redirect('/read-story')
    else:
        return HttpResponseNotFound("HaHa Don't Try To Be Cool") 

# To show clippings
@login_required(login_url='/login/')
def showClippings(request):
    '''To show Clippings (both user and group) '''
    clippedUsers = Clipping.objects.filter(user=request.user)
    clippedGroups = Groupclipping.objects.filter(user=request.user)
    clippedStory = Storyclipping.objects.filter(user =request.user)
    
    user_profiles = Profile.objects.filter(user__in=[user_clipping.visitedUser for user_clipping in clippedUsers])

    context = {
        'clippedUsers': clippedUsers,
        'clippedGroups': clippedGroups,
        'clippedStory': clippedStory,
        'user_profiles': user_profiles,
    }

    return render(request, 'clippings.html', context)


# for push notification (Note: I am copy pasting official docs code)
def send_push_notification(request):
    # Get the user you want to send the notification to
    user = request.user

    # Send a simple notification
    send_user_notification(
        user=user,
        payload={
            'head': 'Notification Title',
            'body': 'Notification Body',
            'icon': '../static/images/logos/g-high-resolution-logo-white-transparent.png',  # Optional: Provide a path to an icon
        },
        ttl=1000  # Time to live for the notification in milliseconds
    )

    return HttpResponse("Push notification sent!")


# Update password systems
def update_password(request):
    return render(request, 'updatePassword.html')