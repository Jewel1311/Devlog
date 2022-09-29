from datetime import datetime
from django.forms import ValidationError
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from core.forms import PostForm, ProfileForm, UserForm, UserRegistrationForm, LoginForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from core.utils import get_read_time, save_tags
from . import decorators
from django.contrib.auth.decorators import login_required
from . models import Posts, Profile, Tags



def home(request):
    posts = Posts.get_recent_posts()
    popular = Posts.get_top_posts()[:5]
    context = {
        'posts':posts,
        'popular':popular
    }
    return render(request, 'core/posts.html',context)


def top_posts(request):
    posts = Posts.get_top_posts()
    popular_tag = Tags.objects.order_by('-count')[0]  #get the tag with high count
    popular = Posts.get_tag_post(popular_tag.id)[:5]
    context = {
        'posts':posts,
        'popular':popular,
        'tag':popular_tag
    }
    return render(request, 'core/posts.html',context)


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
                return redirect('home')
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
        return render(request, 'core/profile.html')

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
