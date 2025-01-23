from datetime import timezone
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

from user.models import m_User
# Create your views here.

@api_view(['POST'])
def register_user(request):
    if request.method=='POST':
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        # Debugging: Check if the incoming request data contains 'username' and 'password'
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        print(password)
        # Debugging: Log the received values for username and password
        print(f"Received username: {username}, password: {password}")

        # Ensure username and password are provided
        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = None

        # Check if the username is an email
        if username and '@' in username:
            try:
                user = m_User.objects.get(email=username)
            except ObjectDoesNotExist:
                # Log if no user is found with the email
                print(f"No user found with email: {username}")
                pass

        # If not found by email, try authenticating by username and password
        if not user:
            user = authenticate(username=username, password=password)
            if user is None:
                # Log if authentication fails
                print(f"Authentication failed for username: {username}")
        
        # Check if user is found and authenticated
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'username':username,'token': token.key}, status=status.HTTP_200_OK)

        # Log invalid credentials case
        print(f"Invalid credentials for username: {username}")
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    # if request.method == 'POST':
    #     username=request.data.get('username')
    #     password=request.data.get('password')

    #     user = None
    #     if '@' in username:
    #         try:
    #             user=m_User.objects.get(email=username)
    #         except ObjectDoesNotExist:
    #             pass

    #     if not user:
    #         user = authenticate(username=username, password=password)

    #     if user:
    #         token, _ = Token.objects.get_or_create(user=user)
    #         return Response({'token': token.key}, status=status.HTTP_200_OK)

    #     return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_user_details(request, pk):
    try:
        # Fetch the user that has not been soft-deleted
        user = m_User.objects.get(pk=pk, deleted_at__isnull=True)
    except m_User.DoesNotExist:
        return Response({'detail': 'user not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Serialize the user object and return the data
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_user(request, pk):
    try:
        # Fetch the user that has not been soft deleted
        user = m_User.objects.get(pk=pk, deleted_at__isnull=True)
    except m_User.DoesNotExist:
        return Response({'detail': 'user not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Soft delete the user by setting deleted_at timestamp
    user.deleted_at = timezone.now()
    user.save()
    return Response({'detail': 'user marked as deleted successfully.'}, status=status.HTTP_200_OK)

@api_view(['PUT', 'PATCH'])
def update_user(request, pk):
    try:
        # Fetch the user that has not been soft deleted
        user = m_User.objects.get(pk=pk, deleted_at__isnull=True)
    except m_User.DoesNotExist:
        return Response({'detail': 'user not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        # Full update: Replace the entire user resource
        serializer = UserSerializer(user, data=request.data)
    elif request.method == 'PATCH':
        # Partial update: Update only the provided fields
        serializer = UserSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
