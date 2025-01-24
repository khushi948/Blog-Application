from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['GET'])
def home(request):
    response={'status':200, 'messgae':'Hi'}
    return Response(response)


# def home_page(request):
#     return render(request,'home.html')
