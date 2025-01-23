from rest_framework import serializers
from user.models import m_User

#user serializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=m_User
        fields=('id','username','email','phone_no','password')

#Register Serializer
class RegisterSerialzer(serializers.ModelSerializer):
    class Meta:
        model=m_User
        fields=('id','username','email','phone_no','password')
        extra_kwargs={'password':{'write_only':'True'}}#whyyyy thissss

    def create(self, validated_data):
        user=m_User.Ojects.create_user(validated_data['username'],email=validated_data['email'],phone_no=validated_data['phone_no'])#WHY THISSS
        user.set_password(validated_data['password'])
        user.save()
        return user
