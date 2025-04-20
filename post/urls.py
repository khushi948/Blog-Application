from django.urls import path
# from post.views import postComment,delete_comment,update_comment,get_comment_details
from django.conf import settings
from django.conf.urls.static import static

from post.views import add_post_view, create_post_api, delete_post_view, like_post_view, post_detail_view, update_post_view, user_profile_view
urlpatterns=[
path('view_profile',user_profile_view, name='user_profile_view'),
path('create-post', create_post_api, name='create_post_api'),
path('add_post_view',add_post_view, name='add_post_view'),
path('post_detail_view/<int:post_id>/', post_detail_view, name='post_detail_view'),
path('update_post_view/<int:post_id>/', update_post_view, name='update_post_view'),
path('delete_post_view/<int:post_id>/', delete_post_view, name='delete_post_view'),
path('post/<int:post_id>/like/', like_post_view, name='like_post'),
]