from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('view_bloggers/', views.view_bloggers, name='view_bloggers'),
    path('admin_blogger_profile/<int:pk>/', views.admin_blogger_profile, name='admin_blogger_profile'),
    path('block_blogger/<int:pk>/', views.block_blogger, name='block_blogger'),
    path('view_post/<int:pk>/', views.view_post, name='view_post'),
    path('post_reports/<str:rpt>/', views.post_reports, name='post_reports'),
    path('block_post/<int:pk>/', views.block_post, name='block_post'),

]