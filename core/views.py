from ast import keyword
import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect
from core.forms import PostForm, ProfileForm, SearchForm, UserForm, UserRegistrationForm, LoginForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from core.utils import get_is_liked, get_read_time, save_tags, get_is_saved
from . import decorators
from django.contrib.auth.decorators import login_required
from . models import Posts, Profile, Tags
from django.contrib.auth.models import User
from django.db.models import Q




#show recent posts, main home
def home(request):
    posts = Posts.get_recent_posts()
    popular = Posts.get_top_posts()[:5]
    is_liked = get_is_liked(posts,request.user)
    is_saved = get_is_saved(posts,request.user)
    context = {
        'posts':posts,
        'popular':popular,
        'is_liked':is_liked,
        'is_saved':is_saved
    }
    return render(request, 'core/posts.html',context)


def top_posts(request):
    posts = Posts.get_top_posts()
    popular_tag = Tags.objects.order_by('-count')[0]  #get the tag with high count
    popular = Posts.get_tag_post(popular_tag.id)[:5]
    is_liked = get_is_liked(posts,request.user)
    is_saved = get_is_saved(posts,request.user)
    context = {
        'posts':posts,
        'popular':popular,
        'tag':popular_tag,
        'is_liked':is_liked,
        'is_saved':is_saved
    }
    return render(request, 'core/posts.html',context)

#blogger home
@login_required
def myfeed(request):
    popular = Posts.get_top_posts()[:5]
    posts = []
    posts_id = []

    #find post id of followers
    for people in request.user.followers.all(): #reverse lookup m2m field using related name
        people_post = Posts.objects.filter(user = people.user, active=True)
        for post in people_post:
            posts_id.append(post.id)

    posts_id.sort(reverse=True) 
  
    for post in posts_id:
        posts.append(Posts.objects.get(pk = post))

    is_liked = get_is_liked(posts,request.user)
    is_saved = get_is_saved(posts,request.user)
    context = {
        'popular':popular,
        'posts':posts,
        'is_liked' :is_liked,
        'is_saved':is_saved
    }
    return render(request,'core/posts.html',context)

def myposts(request,pk):
    posts = Posts.objects.filter(user = pk ,active=True).order_by('-id')
    is_liked = get_is_liked(posts,request.user)
    is_saved = get_is_saved(posts,request.user)
    context ={
        'posts':posts,
        'is_liked' :is_liked,
        'is_saved':is_saved
        
    }
    return render(request, 'core/posts.html',context)

def read_post(request, slug):
    post = Posts.objects.get(slug = slug)
    profile = Profile.objects.get(user = post.user)
    is_liked = False
    is_saved = False
    is_following = False
    if request.user in post.likes.all():
        is_liked = True
    if request.user in post.saved.all():
        is_saved = True
    if request.user in profile.connections.all():
        is_following = True
    context = {
        'post':post,
        'is_liked':is_liked,
        'is_saved':is_saved,
        'is_following':is_following
    }
    return render(request, 'core/readpost.html',context)


@decorators.check_loggedin
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(False)
            user.date_joined = datetime.now()
            user.save()
            return redirect('home')
    else:
        form = UserRegistrationForm
    return render(request, 'core/register.html', {'form':form})


@decorators.check_loggedin
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            passw = form.cleaned_data['password']
            user = authenticate(request,username = uname, password = passw )
            if user:
                login(request,user)
                return redirect('myfeed')
            else:
                messages.error(request,'Invalid credentials')
                return redirect('login_view')
    else:
        form = LoginForm()
    return render(request, 'core/login.html',{'form':form})
    
@login_required
def write_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            body = form.cleaned_data['body']
            tags = form.cleaned_data['tags']

            post_tags = save_tags(tags)
            post = form.save(False)

            post.date = datetime.now()
            post.user = request.user
            post.readtime = get_read_time(body)
            post.save()
            post.tags.add(*post_tags) #add tag id's in post
            post.save()

            #saving no of posts in user profile
            profile = Profile.objects.get(user=request.user)
            profile.post_count +=1 
            profile.save()

            return redirect('home')
    
        return render(request, 'core/write.html',{'form':form})   

    else:
        form = PostForm()
        tags = Tags.objects.all().order_by('-count')[:10]
        context = {
            'form':form, 
            'tags':tags
            }
        return render(request, 'core/write.html',context)   

@login_required  
def blogger_profile(request):
    profile = Profile.objects.get(user = request.user)
    blogger = request.user
    posts = Posts.objects.filter(user = request.user).order_by('-id')[:3]
    context={
        'blogger':blogger,
        'profile':profile,
        'posts':posts
        } 
    return render(request, 'core/profile.html',context)

def view_profile(request,pk):
    profile = Profile.objects.get(user = pk)
    blogger = User.objects.get(pk = pk)
    posts = Posts.objects.filter(user = pk).order_by('-id')[:3]
    is_following = False
    if request.user in profile.connections.all():
        is_following = True
    context={
        'blogger':blogger,
        'profile':profile,
        'posts':posts,
        'is_following':is_following
        } 
    return render(request, 'core/profile.html',context)

@login_required
def edit_profile(request):
    if request.method == "POST":
        uform = UserForm(request.POST, instance=request.user)
        pform = ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if uform.is_valid() and pform.is_valid():
            pform.save()
            uform.save()
            return redirect('blogger_profile')
        else:
            context = {
            'pform':pform,
            'uform':uform
            }
            return render(request, 'core/editprofile.html',context)
    else:
        pform = ProfileForm(instance=request.user.profile)
        uform = UserForm(instance=request.user)
        context = {
            'pform':pform,
            'uform':uform
        }
        return render(request, 'core/editprofile.html',context)

@login_required
def post_likes(request):
    pk = request.GET.get("postid")
    post = Posts.objects.get(pk = pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        post.like_count -=1
        inc = False
    else:
        post.likes.add(request.user)
        post.like_count +=1
        inc = True
    post.save()
    return JsonResponse({'count':post.like_count, 'inc':inc})

@login_required
def post_bookmark(request):
    pk = request.GET.get("postid")
    post = Posts.objects.get(pk = pk)
    if request.user in post.saved.all():
        post.saved.remove(request.user)
        post.save_count -=1
        inc = False
    else:
        post.saved.add(request.user)
        post.save_count +=1
        inc = True
    post.save()
    return JsonResponse({'inc':inc})

@login_required
def view_bookmarked(request):
    posts = Posts.objects.filter(saved = request.user, active = True).order_by('-id')
    is_liked = get_is_liked(posts,request.user)
    is_saved = get_is_saved(posts,request.user)
    context ={
        'posts':posts,
        'is_liked' :is_liked,
        'is_saved':is_saved
        
    }
    return render(request, 'core/posts.html',context)

@login_required
def view_likes(request,pk):
    post = Posts.objects.get(pk=pk)
    context = {
        'post':post
    }
    return render(request, 'core/peopleview.html',context)

@login_required
def followers(request):
    user = request.GET.get('userid')
    profile1 = Profile.objects.get(user = user)
    profile2 = Profile.objects.get(user = request.user)
    if request.user != user:
        if request.user in profile1.connections.all():
            profile1.connections.remove(request.user)
            profile1.followers_count -= 1
            profile2.following_count -= 1
            add = False
        else:
            profile1.connections.add(request.user)
            profile1.followers_count += 1
            profile2.following_count += 1
            add = True

        profile1.save()
        profile2.save()
        return JsonResponse({'fc':profile1.followers_count,'add':add})


def view_followers(request, pk):
    profile = Profile.objects.get(user = pk)
    context = {
        'profile':profile,
        'peoples':profile.connections.all()
    }
    return render(request, 'core/peopleview.html', context)


def view_following(request, pk):
    usr = User.objects.get(pk = pk)
    tags = request.user.tagfollower.all()
    context = {
        'usr':usr,
        'peoples':usr.followers.all(),
        'tags':tags,
        'following':True
    }
    return render(request, 'core/peopleview.html', context)

def search_posts(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data['search']
            posts = Posts.objects.filter(title__icontains=keyword , active=True).order_by('-date')
            is_liked = get_is_liked(posts,request.user)
            is_saved = get_is_saved(posts,request.user)
            context = {
                'posts':posts,
                'form':form,
                'is_liked' :is_liked,
                'is_saved':is_saved
            }

            return render(request, 'core/search.html',context)
    else:
        form = SearchForm()
        context = {
            'form':form
        }
        return render(request, 'core/search.html',context)

def search_people(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data['search']
            peoples = User.objects.filter(Q(username__icontains=keyword) | Q(first_name__icontains=keyword) | Q(first_name__icontains=keyword)).exclude(is_superuser=True)
            context = {
                'peoples':peoples,
                'form':form,
            }

            return render(request, 'core/search.html',context)
    else:
        form = SearchForm()
        context = {
            'form':form
        }
        return render(request, 'core/search.html',context)

def search_tags(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data['search']
            tags = Tags.objects.filter(name__icontains=keyword)
            context = {
                'tags':tags,
                'form':form,
            }

            return render(request, 'core/search.html',context)
    else:
        form = SearchForm()
        context = {
            'form':form
        }
        return render(request, 'core/search.html',context)

def tag_detail(request, slug):
    tag = Tags.objects.get(slug = slug)
    posts = []
    is_following = False
    all_posts = Posts.objects.filter(active = True).order_by('-id')
    for post in all_posts:
        if tag in post.tags.all():
            posts.append(post)
    is_liked = get_is_liked(posts,request.user)
    is_saved = get_is_saved(posts,request.user)
    if request.user in tag.followers.all():
        is_following = True

    context = {
        'tag':tag,
        'posts':posts,
        'is_liked' :is_liked,
        'is_saved':is_saved,
        'is_following':is_following
    }
    return render(request, 'core/tags.html', context)

@login_required
def tag_follow(request):
    tagid = request.GET.get('tagid')
    tag = Tags.objects.get(pk = tagid)
    profile = Profile.objects.get(user = request.user)
    if request.user in tag.followers.all():
        tag.followers.remove(request.user)
        profile.following_count -= 1
        tag.follower_count -= 1
        add = False
    else:
        tag.followers.add(request.user)
        profile.following_count += 1
        tag.follower_count += 1
        add = True
    tag.save()
    profile.save()
    return JsonResponse({'fc':tag.follower_count,'add':add})