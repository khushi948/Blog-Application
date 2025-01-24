from django.urls import path
from post.views import postCategory,getCategory,category_list,deleteCategory,create_post,delete_post,update_post,get_post_details
from post.views import postComment,delete_comment,update_comment,get_comment_details
from post.views import post_list,comment_list,like_post,unlike_post,search_posts,like_unlike_post,get_like_count
from django.conf import settings
from django.conf.urls.static import static

from post.views import home,blog_list,add_comment,post_details
urlpatterns=[
    #APIS
    path('post_category',postCategory,name='postCategory'),
    path('get_category',getCategory,name='get_category'),
    path('category_list', category_list, name='category_list'),
    path('delete_category/<int:pk>',deleteCategory, name='category-soft-delete'),
    # path('images/upload/', ImageUploadView.as_view(), name='image-upload'),
    path('create_post', create_post, name='create_post'),
    path('delete_post/<int:pk>', delete_post, name='delete_post'),
    path('update_post/<int:pk>', update_post, name='update_post'),
    path('get_post_details/<int:pk>', get_post_details, name='get_post_details'),

    path('postComment', postComment, name='create_comment'),
    path('delete_comment/<int:pk>', delete_comment, name='delete_comment'),
    path('update_comment/<int:pk>', update_comment, name='update_comment'),
    path('get_comment_details/<int:pk>', get_comment_details, name='get_comment_details'),

    # path('get_image/<int:pk>/',get_image,name='get_image'),
    # path('delete_image/<int:pk>/',delete_image,name='delete_image'),
    # path('post_image/',post_image,name='post_image'),

    path('search-posts/', search_posts, name='search_posts'),

    path('post_list', post_list, name='post_list'),
    path('comment_list', comment_list, name='comment_list'),

     path('post/<int:post_id>/like/', like_unlike_post, name='like_unlike_post'),
    path('post/<int:post_id>/likes/', get_like_count, name='get_like_count'),

# path('blog1/',blog),

path('',home, name='home'),
    path('blog/',blog_list, name='blog'),
    path('blog/<int:post_id>/',post_details, name='post_details'),
    path('blog/<int:post_id>/add_comment/',add_comment, name='add_comment'),
    # path('api/toggle_like/<int:post_id>/',toggle_like, name='toggle_like'),

    path('like_unlike/<int:post_id>', like_unlike_post, name='like_unlike_post'),
    path('likes/<int:post_id>', get_like_count, name='get_like_count'),



]