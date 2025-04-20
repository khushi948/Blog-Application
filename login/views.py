from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from user.models import m_User
from .serializers import UserSerializer, RegisterSerializer
from django.utils import timezone

# Register User API
@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Login API with Session Management
@api_view(['POST'])
def user_login(request):
    data = request.data

    if not data:
        return Response({"error": "No data provided."}, status=status.HTTP_400_BAD_REQUEST)

    username = data.get('username')
    password = data.get('password')
    print(password)
    if not username or not password:
        return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = m_User.objects.get(username=username)
        
        if user.check_password(password):
            login(request, user)
            return Response({"message": "Login successful."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid password."}, status=status.HTTP_401_UNAUTHORIZED)
    except m_User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

# User Logout API (clear session)
@api_view(['POST'])
def user_logout(request):
    if request.method == 'POST':
        logout(request)  # This will clear the session
        return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)

# Soft Delete User API (mark user as deleted)
@api_view(['DELETE'])
def delete_user(request, pk):
    try:
        user = m_User.objects.get(pk=pk, deleted_at__isnull=True)
    except m_User.DoesNotExist:
        return Response({'detail': 'user not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Soft delete by setting deleted_at timestamp
    user.deleted_at = timezone.now()
    user.save()
    return Response({'detail': 'User marked as deleted successfully.'}, status=status.HTTP_200_OK)

# Update User Details API (with partial update functionality)
@api_view(['PUT', 'PATCH'])
def update_user(request, pk):
    try:
        user = m_User.objects.get(pk=pk, deleted_at__isnull=True)
    except m_User.DoesNotExist:
        return Response({'detail': 'user not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
    elif request.method == 'PATCH':
        serializer = UserSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_details(request, pk):
    try:
        user = m_User.objects.get(pk=pk, deleted_at__isnull=True)
    except m_User.DoesNotExist:
        return Response({'detail': 'user not found.'}, status=status.HTTP_404_NOT_FOUND)
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.decorators import api_view

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        # Call the API view to authenticate user (you can also call the API in the frontend)
        response = user_login(request)
        if response.status_code == 200:
            # If the response is successful, login the user
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')  # Redirect to homepage or dashboard after login
            else:
                return render(request, 'login.html', {'error': 'Invalid credentials.'})
        else:
            # If API login fails, render the login page with the error message
            error_message = response.data.get('error', 'Invalid credentials.')
            return render(request, 'login.html', {'error': error_message})
    
    return render(request, 'login.html')  # Just render the login page for GET request


from django.shortcuts import render, redirect
def register_view(request):
    if request.method == "POST":
        data = {
            'username': request.POST['username'],
            'email': request.POST['email'],
            'password': request.POST['password'],
            'phone_no': request.POST['phone_no']
        }
        
        # Call the register API
        response = register_user(request)
        if response.status_code == 201:
            # Redirect to login after successful registration
            return redirect('login')
        else:
            # If registration fails, render the register page with the error message
            error_message = response.data.get('error', 'Something went wrong')
            return render(request, 'register.html', {'error': error_message})
    
    return render(request, 'register.html')  # Just render the register page for GET request
def user_logout_view(request):
    # Log the user out and redirect to the login page
    logout(request)
    return redirect('login')  # Redirect to login page after logout

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])  # Ensure only authenticated users can access this view
# def protected_view(request):
#     return Response({"message": "You have access to this view."})