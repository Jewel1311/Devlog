from django.shortcuts import render
from django.contrib.auth.models import User
from core.models import Profile
from core.models import Posts, Tags
from . import decorators

@decorators.admin_only
def admin_dashboard(request):
    blogger_count = User.objects.filter(is_superuser = False).count()
    post_count = Posts.objects.filter().count()
    tag_count = Tags.objects.filter().count()
    popular_tag = Tags.objects.order_by('-count')[:5]
    top_bloggers = Profile.objects.filter().order_by('-followers_count')[:5]
    context = {
        'blogger_count': blogger_count,
        'post_count': post_count,
        'tag_count' : tag_count,
        'popular_tag': popular_tag[0],
        'top_bloggers': top_bloggers,
        'top_tags' : popular_tag
    } 
    return render(request,'dev_admin/admin_dashboard.html',context)
