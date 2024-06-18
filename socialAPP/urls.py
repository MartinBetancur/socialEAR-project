from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework import routers, urlpatterns


urlpatterns = [
	path('feed/', views.feed, name='feed'),
    path('', views.index, name='index'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logouto, name='logout'),
    path('keyword/', views.keyword, name='keyword'),
    path('profile-front/', views.profilefront, name='profile-front'),
	path('profile/', views.profile, name='profile'),
	path('profile/<str:username>/', views.profile, name='profile'),
	path('register/', views.register, name='register'),
	path('post/', views.post, name='post'),
    path('editProfile/', views.editProfile, name='editProfile'),
	path('follow/<str:username>/', views.follow, name='follow'),
	path('unfollow/<str:username>/', views.unfollow, name='unfollow'),
    path('linkedin_post/', views.linkedin_post, name='linkedin_post'),
    path('search_posts/', views.search_posts, name='search_posts'),
	
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
