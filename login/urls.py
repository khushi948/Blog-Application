from django.contrib import admin
from django.urls import path
from home.views import home
from django.conf import settings
from django.conf.urls.static import static
from login.views import register_user,user_login,user_logout
from login.views import get_user_details,update_user,delete_user

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    # path('create_user/', create_user, name='create_user'),
    path('delete_user/<int:pk>/', delete_user, name='delete_user'),
    path('update_user/<int:pk>/', update_user, name='update_user'),
    path('get_user_details/<int:pk>/', get_user_details, name='get_user_details'),

   
]

