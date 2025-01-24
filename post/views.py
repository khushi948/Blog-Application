from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from .models import m_Category
from .models import t_Post
# from .models import t_Images
from .models import m_comment
from .serializers import CategorySerializer
# from .serializers import ImageSerializer
# Create your views here.
from .serializers import CommentSerializer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import PostSerializer
from .serializers import CategorySerializer
from rest_framework import filters
from rest_framework import generics
from .serializers import LikeSerializer

def category_list(request):
    # search_fields = ['name']
    # filter_backends = (filters.SearchFilter,)
    categories=m_Category.objects.all()
    if request.method=="GET":
        category_name=request.GET.get('name')
        if category_name:
            new_category = m_Category.objects.create(name=category_name)
            return redirect('category_list')  # Redirect to the same page to see the new category
    return render (request,'category_list.html',{'categories':categories})
    
@api_view(['POST'])
def postCategory(request):
    if request.method=='POST':
        serializer=CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getCategory(request):
    if request.method=='GET':
        obj=m_Category.objects.all()
        serializer=CategorySerializer(obj, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
def deleteCategory(request,pk):
    try:
        category = m_Category.objects.get(pk=pk, deleted_at__isnull=True)  # Only fetch non-deleted categories
    except m_Category.DoesNotExist:
        return Response({'detail': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)

    category.soft_delete()  # Perform soft delete by setting the deleted_at timestamp
    return Response({'detail': 'Category marked as deleted successfully.'}, status=status.HTTP_200_OK)
# class ImageUploadView(APIView):
#     parser_classes = [MultiPartParser, FormParser]

#     def post(self, request, *args, **kwargs):
#         serializer = ImageSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def create_post(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_post(request, pk):
    try:
        # Fetch the post that has not been soft deleted
        post = t_Post.objects.get(pk=pk, deleted_at__isnull=True)
    except t_Post.DoesNotExist:
        return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Soft delete the post by setting deleted_at timestamp
    post.deleted_at = timezone.now()
    post.save()
    return Response({'detail': 'Post marked as deleted successfully.'}, status=status.HTTP_200_OK)

@api_view(['PUT', 'PATCH'])
def update_post(request, pk):
    try:
        # Fetch the post that has not been soft deleted
        post = t_Post.objects.get(pk=pk, deleted_at__isnull=True)
    except t_Post.DoesNotExist:
        return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        # Full update: Replace the entire post resource
        serializer = PostSerializer(post, data=request.data)
    elif request.method == 'PATCH':
        # Partial update: Update only the provided fields
        serializer = PostSerializer(post, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_post_details(request, pk):
    try:
        # Fetch the post that has not been soft-deleted
        post = t_Post.objects.get(pk=pk, deleted_at__isnull=True)
    except t_Post.DoesNotExist:
        return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Serialize the post object and return the data
    serializer = PostSerializer(post)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['POSt'])
def postComment(request):
    if request.method=='POST':
        serializer=CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)




@api_view(['DELETE'])
def delete_comment(request, pk):
    try:
        # Fetch the comment that has not been soft deleted
        comment = m_comment.objects.get(pk=pk, deleted_at__isnull=True)
    except m_comment.DoesNotExist:
        return Response({'detail': 'comment not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Soft delete the comment by setting deleted_at timestamp
    comment.deleted_at = timezone.now()
    comment.save()
    return Response({'detail': 'comment marked as deleted successfully.'}, status=status.HTTP_200_OK)

@api_view(['PUT', 'PATCH'])
def update_comment(request, pk):
    try:
        # Fetch the comment that has not been soft deleted
        comment = m_comment.objects.get(pk=pk, deleted_at__isnull=True)
    except m_comment.DoesNotExist:
        return Response({'detail': 'comment not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        # Full update: Replace the entire comment resource
        serializer = CommentSerializer(comment, data=request.data)
    elif request.method == 'PATCH':
        # Partial update: Update only the provided fields
        serializer = CommentSerializer(comment, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_comment_details(request, pk):
    try:
        # Fetch the comment that has not been soft-deleted
        comment = m_comment.objects.get(pk=pk, deleted_at__isnull=True)
    except m_comment.DoesNotExist:
        return Response({'detail': 'comment not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Serialize the comment object and return the data
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_200_OK)



# @api_view(['GET'])
# def get_image(request,pk):
#     try:
#         img=t_Images.objects.get(pk=pk,deleted_at__isnull=True)
#     except t_Images.DoesNotExist:
#         return Response({'detail':'Image not found'},status=status.HTTP_404_NOT_FOUND)
    
#     serializer=ImageSerializer(img)

#     return Response(serializer.data,status=status.HTTP_200_OK)


# @api_view(['DELETE'])
# def delete_image(request,pk):
#     try:
#         img=t_Images.objects.get(pk=pk,deleted_at__isnull=True)
#     except t_Images.DoesNotExist:
#         return Response({'detail': 'image not found.'},status=status.HTTP_404_NOT_FOUND)

#     img.delete_at=timezone.now()
#     img.save()

#     return Response({'detail': 'image marked as deleted successfully.'}, status=status.HTTP_200_OK)


# @api_view(['POST'])
# def post_image(request):
#     file=request.data('file')
    # image = t_Images.objects.create(image=file)
        
    # serializer=ImageSerializer()
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response(serializer.data,{"message":"image uploaded successfully"},status=status.HTTP_200_OK)
    
    # return Response({'message':'could not upload image','error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)


def post_list(request):
    
    posts=t_Post.objects.all()
    if request.method=="POST":
        post_name=request.POST.get('name')
        if post_name:
            new_post = t_Post.objects.create(name=post_name)
            return redirect('post')  # Redirect to the same page to see the new post
    return render (request,'view_post.html',{'posts':posts})
    


def comment_list(request):
    comments=m_comment.objects.all()
    if request.method=="POST":
        comment_name=request.POST.get('name')
        if comment_name:
            new_comment = m_comment.objects.create(name=comment_name)
            return redirect('view_comments')  # Redirect to the same page to see the new comment
    return render (request,'view_comments.html',{'comments':comments})

# def blog(request):
#     posts=t_Post.objects.all()
#     comments=m_comment.objects.all()
#     if request.method=="POST":
#         post_name=request.POST.get('name')
#         comment_name=request.POST.get('message')
#         if post_name:
#             new_post = t_Post.objects.create(name=post_name)

#             return redirect('post')
#     return render(request,'base.html',{'posts':posts,'comments':comments})

# @login_required
def like_post(request, post_id):
    post = get_object_or_404(t_Post, id=post_id)

    # Check if the user has already liked the post in their session
    if request.session.get(f"liked_post_{post.id}", False):
        # If the post is already liked, do nothing
        return redirect('/api_post/post/', post_id=post.id)

    # Mark the post as liked by the user in the session
    request.session[f"liked_post_{post.id}"] = True
    
    # Safely increment the like count
    t_Post.likes = t_Post.likes + 1  # Increment like count
    post.save(update_fields=["likes"])  # Save only the "likes" field

    return redirect('/api_post/post/<int:pk>', post_id=post.id)

# @login_required
def unlike_post(request, post_id):
    post = get_object_or_404(t_Post, id=post_id)

    # Check if the user has liked the post in their session
    if request.session.get(f"liked_post_{post.id}", False):
        # Decrement the like count and mark the post as unliked
        t_Post.likes = t_Post.likes - 1  # Decrement like count
        post.save(update_fields=["likes"])  # Save only the "likes" field
        del request.session[f"liked_post_{post.id}"]  # Remove the like from the session

    return redirect('/api_post/post/<int:pk>', post_id=post.id)
    return redirect('/api_post/post/<int:pk>', post_id=post.id)
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import t_Post, m_comment,m_User
from django.views.decorators.csrf import csrf_exempt
import json

def home(request):
    # latest_posts = t_Post.objects.order_by('-created_at')[:5]

    query = request.GET.get('query', '')
    if query:
        posts = t_Post.objects.filter(title__icontains=query)
    else:
        posts = t_Post.objects.all()
    return render(request, 'base1.html', {'posts': posts})

    # return render(request, 'base.html', {'latest_posts': latest_posts})

# Blog list view
def blog_list(request):
    query = request.GET.get('query', '')
    if query:
        posts = t_Post.objects.filter(title__icontains=query)
    else:
        posts = t_Post.objects.all()
    return render(request, 'blog.html', {'posts': posts})

# Blog details view
def post_details(request, post_id):
    post = get_object_or_404(t_Post, id=post_id)
    return render(request, 'post_details.html', {'post': post})

# Add comment view
def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(t_Post, id=post_id)
        content = request.POST.get('content')
        m_comment.objects.create(post=post, author=request.m_User, content=content)
        return redirect('post_details', post_id=post_id)

# Toggle like view (API endpoint)
# @csrf_exempt
# def toggle_like(request, post_id):
#     if request.method == 'POST':
#         post = get_object_or_404(t_Post, id=post_id)
#         data = json.loads(request.body)
#         liked = data.get('liked', False)
#         if liked:
#             post.likes -= 1
#         else:
#             post.likes += 1
#         post.save()
#         return JsonResponse({'likes': post.likes, 'liked': not liked})
    

@api_view(['GET'])
def search_posts(request):
    keyword = request.GET.get('keyword', '')
    if not keyword:
        return Response({'error': 'Keyword is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Search posts by title or description
    posts = t_Post.objects.filter(
        Q(title__icontains=keyword) | Q(description__icontains=keyword)
    )

    # Serialize the data
    serializer = PostSerializer(posts, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def like_unlike_post(request, post_id):
    try:
        post = t_Post.objects.get(id=post_id)
    except t_Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = LikeSerializer(data=request.data)
    if serializer.is_valid():
        flag = serializer.validated_data['flag']
        if flag:
            post.likes += 1  # Increment the like count
        elif post.likes > 0:
            post.likes -= 1  # Decrement the like count (ensure it's not negative)
        post.save()
        return Response({'message': 'Like count updated', 'likes': post.likes}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_like_count(request, post_id):
    try:
        post = t_Post.objects.get(id=post_id)
    except t_Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'likes': post.likes}, status=status.HTTP_200_OK)
    