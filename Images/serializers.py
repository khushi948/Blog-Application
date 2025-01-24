from rest_framework import serializers
from Images.models import t_Images


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=t_Images
        fields=['images','post_id']

