from django.urls import path
from post.views import postCategory,getCategory,category_list,deleteCategory,create_post,delete_post,update_post,get_post_details
from post.views import postComment,delete_comment,update_comment,get_comment_details
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('post_category',postCategory,name='postCategory'),
    path('get_category',getCategory,name='get_category'),
    path('category_list', category_list, name='category_list'),
    path('delete_category/<int:pk>',deleteCategory, name='category-soft-delete'),
    # path('images/upload/', ImageUploadView.as_view(), name='image-upload'),
    path('create_post/', create_post, name='create_post'),
    path('delete_post/<int:pk>/', delete_post, name='delete_post'),
    path('update_post/<int:pk>/', update_post, name='update_post'),
    path('get_post_details/<int:pk>/', get_post_details, name='get_post_details'),

    path('postComment/', postComment, name='create_comment'),
    path('delete_comment/<int:pk>/', delete_comment, name='delete_comment'),
    path('update_comment/<int:pk>/', update_comment, name='update_comment'),
    path('get_comment_details/<int:pk>/', get_comment_details, name='get_comment_details'),


]