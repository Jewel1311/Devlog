from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('',views.home, name='home'),
    path('top_posts',views.top_posts, name='top_posts'),
    path('write_post',views.write_post, name='write_post'),
    path('blogger_profile',views.blogger_profile, name='blogger_profile'),
    path('view_profile/<int:pk>/',views.view_profile, name='view_profile'),
    path('edit_profile',views.edit_profile, name='edit_profile'),
    path('myfeed',views.myfeed, name='myfeed'),
    path('myposts/<int:pk>',views.myposts, name='myposts'),
    path('read_post/<slug:slug>/',views.read_post, name='read_post'),
    path('post_likes/',views.post_likes, name='post_likes'),
    path('post_bookmark/',views.post_bookmark, name='post_bookmark'),
    path('view_bookmarked/',views.view_bookmarked, name='view_bookmarked'),
    path('view_likes/<int:pk>/',views.view_likes, name='view_likes'),
    path('followers/',views.followers, name='followers'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)