from rest_framework import serializers
from user.models import m_User
from django.contrib.auth import get_user_model
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = m_User
        fields = ('id', 'username', 'email', 'phone_no', 'password')
# login/serializers.py


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = m_User
        fields = ['username', 'email', 'password', 'phone_no']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = m_User(**validated_data)
        user.password = password  # Leave it raw
        user.save() 
        return user
