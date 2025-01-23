from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.utils import timezone
from rest_framework import status
from .models import m_Category
from .models import t_Post
from .models import t_Image
from .models import t_Comment
from .serializers import CategorySerializer
# Create your views here.
from .serializers import CommentSerializer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import PostSerializer
from .serializers import CategorySerializer

from rest_framework import generics

def category_list(request):
    categories=m_Category.objects.all()
    if request.method=="POST":
        category_name=request.POST.get('name')
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
        comment = t_Comment.objects.get(pk=pk, deleted_at__isnull=True)
    except t_Comment.DoesNotExist:
        return Response({'detail': 'comment not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Soft delete the comment by setting deleted_at timestamp
    comment.deleted_at = timezone.now()
    comment.save()
    return Response({'detail': 'comment marked as deleted successfully.'}, status=status.HTTP_200_OK)

@api_view(['PUT', 'PATCH'])
def update_comment(request, pk):
    try:
        # Fetch the comment that has not been soft deleted
        comment = t_Comment.objects.get(pk=pk, deleted_at__isnull=True)
    except t_Comment.DoesNotExist:
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
        comment = t_Comment.objects.get(pk=pk, deleted_at__isnull=True)
    except t_Comment.DoesNotExist:
        return Response({'detail': 'comment not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Serialize the comment object and return the data
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_200_OK)
