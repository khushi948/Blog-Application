from django.urls import path
from .views import upload_image, get_image, delete_image

urlpatterns = [
    path('upload', upload_image, name='image-upload'),
    path('get_image/<int:pk>', get_image, name='image-detail'),
    path('delete_image/<int:pk>', delete_image, name='image-delete'),
]
