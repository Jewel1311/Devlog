from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from core.models import Profile
from core.models import Posts, Tags
from devlog_admin.utils import get_post_graph
from . import decorators

@decorators.admin_only
def admin_dashboard(request):
    blogger_count = User.objects.filter(is_superuser = False).count()
    post_count = Posts.objects.filter().count()
    tag_count = Tags.objects.filter().count()
    popular_tag = Tags.objects.order_by('-count')[:5]
    top_bloggers = Profile.objects.filter().order_by('-followers_count')[:5]
    post_graph = get_post_graph()
    context = {
        'blogger_count': blogger_count,
        'post_count': post_count,
        'tag_count' : tag_count,
        'popular_tag': popular_tag[0],
        'top_bloggers': top_bloggers,
        'top_tags' : popular_tag,
        'post_graph':post_graph
    } 
    return render(request,'dev_admin/admin_dashboard.html',context)

@decorators.admin_only
def view_bloggers(request):
    bloggers = User.objects.filter(is_superuser = False).order_by('-id')
    context = {
        'bloggers' : bloggers
    }
    return render(request, 'dev_admin/bloggers.html', context)

@decorators.admin_only
def admin_blogger_profile(request,pk):
    try:
        blogger = User.objects.get(id = pk)
        posts = Posts.objects.filter(user = pk, draft=False)
        drafts = Posts.objects.filter(user = pk, draft=True)
        context = {
            'blogger': blogger,
            'posts': posts,
            'drafts':drafts
        }
        return render(request, 'dev_admin/blogger_profile.html',context)
    except:
        return HttpResponseNotFound('<h2>400 - Bad request</h2>') 
    

@decorators.admin_only
def block_blogger(request, pk):
    try:
        blogger = User.objects.get(id = pk)
        if blogger.is_active:
            blogger.is_active = False
        else:
            blogger.is_active = True
        blogger.save()
        return redirect('admin_blogger_profile', pk = pk)
    except:
        return HttpResponseNotFound('<h2>400 - Bad request</h2>')