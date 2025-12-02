from rest_framework import serializers
from users.models import UserInfo

# 用户信息表序列化
class UserInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = '__all__'