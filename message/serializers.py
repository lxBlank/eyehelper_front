from rest_framework import serializers
from message.models import MessageInfo

# 用户信息表序列化
class MessageInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageInfo
        fields = '__all__'