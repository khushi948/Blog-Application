from http.client import HTTPResponse
from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer
from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from .models import m_Category
from .models import t_Post
from .models import m_comment
from .serializers import CategorySerializer
from .serializers import CommentSerializer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import PostSerializer
from rest_framework import filters
from rest_framework import generics
from .serializers import LikeSerializer


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import t_Post

@login_required
def user_profile_view(request):
    user = request.user
    print(user)
    posts = t_Post.objects.filter(user_id=user, deleted_at=None).order_by('created_at')
    return render(request, 'user_profile.html', {'posts': posts})

# views.py (APIView or function-based)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from post.models import t_Post
from .serializers import PostSerializer
from images.models import t_Images  # if image model exists

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post_api(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        post = serializer.save(user_id=request.user)  # Save user

        # Handle image (if coming from request.FILES)
        image = request.FILES.get('image')
        if image:
            t_Images.objects.create(post_id=post, images=image)

        return Response({'status': 'Post created successfully'})
    return Response(serializer.errors, status=400)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from post.models import m_Category

@login_required
def add_post_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category_id')
        image = request.FILES.get('image')

        if title and description and category_id:
            category = m_Category.objects.get(id=category_id)
            post = t_Post.objects.create(
                user_id=request.user,
                title=title,
                description=description,
                category_id=category,
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            if image:
                t_Images.objects.create(post_id=post, images=image)
            return redirect('user_profile_view')  # or wherever you want
        else:
            return render(request, 'add_post.html', {
                'error': 'Please fill in all fields.',
                'categories': m_Category.objects.filter(deleted_at__isnull=True)
            })
    else:
        categories = m_Category.objects.filter(deleted_at__isnull=True)
        return render(request, 'add_post.html', {'categories': categories})
    
def post_detail_view(request, post_id):
    try:
        post = t_Post.objects.get(id=post_id, deleted_at__isnull=True)
        images = t_Images.objects.filter(post_id=post)
        # return render(request, 'post_detail.html', {'post': post})
   
    
        return render(request, 'post_detail.html', {'post': post, 'post_images': images})
    except t_Post.DoesNotExist:
        return HTTPResponse("Post not found", status=404)
from django.shortcuts import get_object_or_404

def update_post_view(request, post_id):
    post = get_object_or_404(t_Post, id=post_id, deleted_at__isnull=True)

    if request.method == 'POST':
        post.title = request.POST['title']
        post.description =  request.POST.get('description')
        post.category_id_id = request.POST.get('category_id')
        post.updated_at = timezone.now()
        post.save()
        return redirect('post_detail_view', post_id=post.id)

    categories = m_Category.objects.filter(deleted_at__isnull=True)
    return render(request, 'update_post.html', {'post': post, 'categories': categories})

def delete_post_view(request, post_id):
    post = get_object_or_404(t_Post, id=post_id, deleted_at__isnull=True)
    post.soft_delete()
    post.deleted_at=timezone.now()
    return redirect('user_profile_view')  # redirect to profile or post list


def like_post_view(request, post_id):
    post = get_object_or_404(t_Post, id=post_id, deleted_at__isnull=True)

   
    liked_posts = request.session.get('liked_posts', [])
    if post_id not in liked_posts:
        post.likes += 1
        post.save()
        liked_posts.append(post_id)
        request.session['liked_posts'] = liked_posts

    return redirect('post_detail_view', post_id=post_id)