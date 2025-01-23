from rest_framework import serializers
from post.models import m_Category
# from post.models import t_Image
from post.models import t_Post
from post.models import t_Comment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=m_Category
        fields = ['name', 'deleted_at']
        extra_kwargs = {
            'deleted_at': {'read_only': True}
        }

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=t_Comment
        fields=['user_id','post_id','message']



# class ImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=t_Image
#         fields=['id','image']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=t_Post
        fields=['user_id','category_id','title','description']