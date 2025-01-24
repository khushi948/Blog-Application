from django.shortcuts import render


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .models import t_Images
from .serializers import ImageSerializer


# Create your views here.

@api_view(['POST'])
def upload_image(request):
    if request.method == 'POST':
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_image(request, pk):
    try:
        image = t_Images.objects.get(pk=pk)
    except t_Images.DoesNotExist:
        return Response({"error": "Image not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ImageSerializer(image)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_image(request, pk):
    try:
        image = t_Images.objects.get(pk=pk)
    except t_Images.DoesNotExist:
        return Response({"error": "Image not found."}, status=status.HTTP_404_NOT_FOUND)

    image.soft_delete()
    return Response({"message": "Image marked as deleted."}, status=status.HTTP_204_NO_CONTENT)
