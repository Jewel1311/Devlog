from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('view_bloggers/', views.view_bloggers, name='view_bloggers'),
    path('admin_blogger_profile/<int:pk>/', views.admin_blogger_profile, name='admin_blogger_profile'),
    path('block_blogger/<int:pk>/', views.block_blogger, name='block_blogger')
]