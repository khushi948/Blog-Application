from django.contrib import admin
from django.urls import path
from home.views import home
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import HttpResponse
from login import views


urlpatterns = [

    path('api_login/logout', views.user_logout, name='user_logout'),
    path('delete_user/<int:pk>', views.delete_user, name='delete_user'),
    path('update_user/<int:pk>', views.update_user, name='update_user'),
    path('get_user_details/<int:pk>', views.get_user_details, name='get_user_details'),
   
    path('login/', views.login_view, name='login'), 
    path('register/', views.register_view, name='register'),  
     path('logout/', views.user_logout_view, name='logout'),  
    path('api_login/login/', views.user_login, name='api_login'), 
    path('api_login/register/', views.register_user, name='api_register'), 

]