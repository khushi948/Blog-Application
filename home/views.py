from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from post.models import t_Post 
from images.models import t_Images # Make sure you import your Post model

@api_view(['GET'])
def home_api(request):
    user = request.user
    if user.is_authenticated:
        return Response({"message": f"Welcome {user.username}!", "is_logged_in": True}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Welcome to the Home Page! Please log in.", "is_logged_in": False}, status=status.HTTP_200_OK)

def home(request):
    if request.user.is_authenticated:
        # Fetch latest 3 non-deleted posts
        posts = t_Post.objects.filter(deleted_at__isnull=True).order_by('-created_at')[:3]
        return render(request, 'logged_in_home.html', {
            'username': request.user.username,
            'posts': posts
        })
    else:
        posts = t_Post.objects.filter(deleted_at__isnull=True).order_by('-created_at')[:3]
        return render(request, 'home.html', {
            'posts': posts
        })
        

def all_posts_view(request):
    posts = t_Post.objects.filter(deleted_at=None).order_by('-created_at')
    images = t_Images.objects.filter(post_id__in=posts)

    return render(request, 'all_post.html', {
        'posts': posts,
        'post_images': images
    })