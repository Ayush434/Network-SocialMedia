from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms


from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from.models import Posts, Followers, Following, Likes, User
from django.core import serializers
from django.core.paginator import Paginator
from django.views.generic import ListView
from annoying.functions import get_object_or_None
from django.db.models import F

# this func returns the posts if any otherwise None so the index.html knows either to show posts or a message
def index(request):
    
    try:
        posts = Posts.objects.all()
    except Posts.DoesNotExist:
        posts = None
    
    return render(request, "network/index.html",{
        "page_obj": posts
    })
    
# This func returns the posts to the index.js in order to show the posts
def show_posts(request, endpoint):
    
    # get all the posts if any
    try:
        posts = Posts.objects.all()
    except Posts.DoesNotExist:
        return HttpResponse(status=404) 
    
    # Change the order of posts by time and then do the following for pagination
    posts = posts.order_by("-timestamp").all()
    paginator = Paginator(posts, 10)
    
    counter = int(request.GET.get("page") or 1)
    
    # send the posts
    if endpoint == "posts":
        page = paginator.page(counter)
        set_posts = page.object_list
        return JsonResponse([post.serialize() for post in set_posts], safe=False)
    
    # send the number of pages
    elif endpoint == "pages":
        return JsonResponse({"pages": paginator.num_pages})
    
    # if any other endpoint than raise the error
    else:
        return HttpResponse(status=404) 
    
def getLikedPosts(request):
    if request.user.is_authenticated:
        user_obj = User.objects.get(id=request.user.id)
        likeobj = Likes.objects.values_list('post', flat=True).filter(user=user_obj.id)
        postobj = Posts.objects.filter(id__in = set(likeobj)).order_by('-timestamp').values()
        
        
        return postobj
    else:
        return HttpResponseRedirect(reverse("login"))
        
# This function sends the posts to profile.js getposts()
@login_required
def profilePosts(request, endpoint):
    
    # get user's username and check if user has created any posts
    username = request.user.username
    userHasPosts = Posts.objects.filter(user=username).exists()
    
    # if user has posts than get them
    if userHasPosts:
        userPosts = Posts.objects.filter(user=username)
    
    # 10 posts per page
    paginator = Paginator(userPosts, 10)
    counter = int(request.GET.get("page") or 1)
    
    
    if endpoint == "posts":
        page = paginator.page(counter)
        set_posts = page.object_list
        return JsonResponse([post.serialize() for post in set_posts], safe=False)
    
    elif endpoint == "pages":
        return JsonResponse({"pages": paginator.num_pages})
    
    else:
        return HttpResponse(status=404) 
    


# if the username link on the post is clicked than this function will be triggered
@login_required
def profileIndex(request, username):
    
    # check if the user who is logged in is checking his/her profile or someone else
    realuser = request.user.username
    if username == realuser:
        me = True
        followers = Followers.objects.filter(user=realuser).count()
        following = Following.objects.filter(user=realuser).count()
        
        userHasPosts = Posts.objects.filter(user=username).exists()

        userFollowing = False
    else:
        me = False
        followers = Followers.objects.filter(user=username).count()
        following = Following.objects.filter(user=username).count()            
            
        userHasPosts = Posts.objects.filter(user=username).exists()        
            
        # check whether the realuser is follwoing the username or not        
        userFollowing = Followers.objects.filter(user=username, follower=realuser).exists()
        
    return render(request, "network/profile.html",{
        "me": me,
        "username": username,
        "followers": followers,
        "following": following,
        "userHasPosts": userHasPosts,
        "userFollowing": userFollowing
    })

@csrf_exempt
@login_required
def updateLikes(request, postId):
    print("Updating Likes")
    
    # Query for Post
    try:
        postObj = Posts.objects.get(pk=postId)
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)

    print(f"Post found here {postObj}")
    
    if request.method == "PUT":
        print("PUT")
        
        user_obj = User.objects.get(id=request.user.id)
        
        user_liked_post_ids = getLikedPosts(request).values_list('id', flat=True)
        print(user_liked_post_ids)
        
        data = json.loads(request.body)
        
        if len(user_liked_post_ids) > 0 and len(user_liked_post_ids.filter(id = postId))>0:
            likeobj = Likes.objects.filter(user = user_obj.id).filter(post=postId)
            #delete
            likeobj = likeobj.delete()

            #reduce like count by 1
            postObj.num_of_likes = F('num_of_likes')-1
            postObj.save()
            return HttpResponse(status=204)
        
        else:
            
            if data.get("like") is not None:
                print("in progress")
                user_to_be = User.objects.filter(id = user_obj.id)
                obj = Likes.objects.create(post = postObj)
                obj.user.set(user_to_be)
                
                 #add like count by 1
                postObj.num_of_likes = F('num_of_likes')+1
                postObj.save()
                
                return HttpResponse(status=204)
            
        
        
    else:
        return HttpResponseRedirect(reverse("login"))
    

@csrf_exempt
@login_required
def postLikedByUser(request, postId):
    # print("Checking if User liked Post")
    
    # Query for Post
    try:
        postObj = Posts.objects.get(pk=postId)
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)

    # print(f"Post found here {postObj}")
    
    if request.method == "GET":
        print("GET")
        
        user_obj = User.objects.get(id=request.user.id)
        
        user_liked_post_ids = getLikedPosts(request).values_list('id', flat=True)
        result = {}
        
        if postId in user_liked_post_ids:
            result["liked"]=True
            
            # generate response
            response = json.dumps(result,default=str) 
            
            return HttpResponse(response,content_type = "application/json")
        
        else:
            result["liked"]=False
            
            # generate response
            response = json.dumps(result,default=str) 
            
            return HttpResponse(response,content_type = "application/json")     
        
       
@login_required
def followingIndex(request):
    return render(request, "network/following.html")  
  

@login_required
def userFollowingPosts(request, endpoint):
    
    if request.user.is_authenticated:
        realuser = request.user.username
        
        userFollowing = Following.objects.filter(user=realuser)
        
        listOfFollowing = []
        
        for i in userFollowing:
            listOfFollowing.append(i.following)
            
        posts = []
        
        for eachUser in listOfFollowing:
            if Posts.objects.filter(user=eachUser).exists():
                eachUserPosts = list(Posts.objects.filter(user=eachUser).order_by("-timestamp").all())
                posts += (eachUserPosts)
        
        paginator = Paginator(posts, 10)
        counter = int(request.GET.get("page") or 1)

        if endpoint == "posts":
            print("here")
            page = paginator.page(counter)
            set_posts = page.object_list
            p  = [post.serialize() for post in set_posts]
            print(p)
            return JsonResponse([post.serialize() for post in set_posts], safe=False)

        elif endpoint == "pages":
            return JsonResponse({"pages": paginator.num_pages})
    
        else:
            return HttpResponse(status=404) 




@login_required
def follow(request, username):
    if request.method == "POST":
        
        realuser = request.user.username
        personToFollow = username
        
        obj = Followers.objects.create(user=personToFollow,
                                       follower=realuser)
        
        obj.save()
        obj2 = Following.objects.create(user=realuser,
                                        following=personToFollow)
        
        obj2.save()
        
        return HttpResponseRedirect(reverse("profileIndex", args=(request.user.username,)))


@login_required
def unfollow(request, username):
    if request.method == "POST":
        
        realuser = request.user.username
        personToFollow = username
        
        obj = Followers.objects.get(user=personToFollow,
                                       follower=realuser)
        
        obj.delete()
        
        obj2 = Following.objects.get(user=realuser,
                                        following=personToFollow)
        
        obj2.delete()
        
        print(username, request.user.username)
        return HttpResponseRedirect(reverse("profileIndex", args=(request.user.username,)))


@csrf_exempt
@login_required
def save_post(request):
    
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # Check the content    
    data = json.loads(request.body)
    
    content = data.get("content", "")
    
    if content == "" or content == " ":        
        return JsonResponse({"error": "Post Content cannot be empty"}, status=400)
    
    user = request.user.username
    description = content
    
    obj = Posts()
    obj.user = user
    obj.description = content


    obj.save()
    
    return JsonResponse({"message": "Post is saved"}, status=201)    

@csrf_exempt
@login_required
def update_post(request):
    
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # Check the content
    
    data = json.loads(request.body)
    
    content = data.get("content", "")
    id = data.get("postId", "")
    
    if content == "" or content == " ":
        
        return JsonResponse({"error": "Post Content cannot be empty"}, status=400)
    
    user = request.user.username
    description = content
    
    obj = Posts.objects.get(pk = id)
    
    if obj.user != request.user.username:
        return JsonResponse({"error": "User is not authorized"}, status=400)
    obj.description = content
    obj.save()
    
    updatedPost = Posts.objects.filter(pk = id)
   
    return JsonResponse({"updatedPost": [post.serialize() for post in updatedPost]}, status=201 )  
    

def currentUser(request):
    return JsonResponse({"username": request.user.username}, status=201)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
