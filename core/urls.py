from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('',views.home, name='home'),
    path('top_posts',views.top_posts, name='top_posts'),
    path('write_post',views.write_post, name='write_post'),
    path('blogger_profile',views.blogger_profile, name='blogger_profile'),
    path('edit_profile',views.edit_profile, name='edit_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)