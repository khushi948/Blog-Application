from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # The function view for the home page
    path('api_home/', views.home_api, name='home_api'),  # The API view for the home page
    path('all_posts/', views.all_posts_view, name='all_posts_view'),

]
