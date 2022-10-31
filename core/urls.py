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
    path('view_followers/<int:pk>/',views.view_followers, name='view_followers'),
    path('view_following/<int:pk>/',views.view_following, name='view_following'),
    path('search_posts/',views.search_posts, name='search_posts'),
    path('search_people/',views.search_people, name='search_people'),
    path('search_tags/',views.search_tags, name='search_tags'),
    path('tag_detail/<slug:slug>/',views.tag_detail, name='tag_detail'),
    path('tag_follow/',views.tag_follow, name='tag_follow'),
    path('edit_post/<int:pk>/',views.edit_post, name='edit_post'),
    path('delete_post/<int:pk>/',views.delete_post, name='delete_post'),
    path('add_comment/',views.add_comment, name='add_comment'),
    path('reply_comment/',views.reply_comment, name='reply_comment'),
    path('change-password/', views.PasswordChangeView.as_view(),name='change-password'),
    path('report_post/<int:pk>/',views.report_post, name='report_post'),
    path('delete_comment/<int:pk>/',views.delete_comment, name='delete_comment'),
    path('delete_reply/<int:pk>/',views.delete_reply, name='delete_reply'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)