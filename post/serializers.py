from rest_framework import serializers
from post.models import m_Category
# from post.models import t_Images
from post.models import t_Post
from post.models import m_comment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=m_Category
        fields = ['name', 'deleted_at']
        extra_kwargs = {
            'deleted_at': {'read_only': True}
        }

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=m_comment
        fields=['user_id','post_id','message']



# class ImageSerializer(serializers.ModelSerializer):
#     # image_url = serializers.ImageField(required=False)
#     class Meta:
#         model=t_Images
#         fields=['id','images']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=t_Post
        fields=['user_id','category_id','title','description']

class LikeSerializer(serializers.Serializer):
    flag = serializers.BooleanField()  # Expect a boolean flag
