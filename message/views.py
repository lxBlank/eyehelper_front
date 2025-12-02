from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.response import Response
from tools import muid, my_token, redis_pool
from message.models import MessageInfo
from message.serializers import MessageInfoModelSerializer
import time
import redis

# Create your views here.

class MessageViewSet(viewsets.ViewSet):
    # 保存消息数据
    @method_decorator(my_token.logging_check)
    def createMessage(self, request):
        user = request.user
        data = request.data.copy()
        data['muid'] = muid.getUid()
        data['uid'] = user.uid
        data['timestamp'] = int(time.time())
        messageInfo = MessageInfoModelSerializer(data=data)
        # 数据保存
        if(messageInfo.is_valid()):
            # 数据存入数据库
            messageInfo.save()
            # 数据存入redis
            r = redis.Redis(connection_pool=redis_pool.pool, decode_responses=True)
            rdata = r.get(user.uid)
            if rdata:
                rdata = rdata.decode('utf-8')
                infoQueue = rdata.split('|')
                infoQueue.append(data['muid'])
                tmp = '|'.join(infoQueue)
                r.set(user.uid, tmp)
            else:
                r.set(user.uid, data['muid'])

        else:
            return Response({'msg': {'error': messageInfo.errors}, 'code': -1})

        res_json = {'data': messageInfo.data, 'msg': 'ok', 'code': 1}
        return Response(res_json)

    @method_decorator(my_token.logging_check)
    def getMessage(self, request):
        user = request.user
        uid = user.uid
        # redis中查询是否有消息
        r = redis.Redis(connection_pool=redis_pool.pool, decode_responses=True)
        rdata = r.get(uid)
        # 有消息
        if rdata:
            rdata = rdata.decode('utf-8')
            infoQueue = rdata.split('|')
            muid = infoQueue.pop(0)

            r.set(uid, '|'.join(infoQueue))
            try:
                messageData = MessageInfo.objects.get(muid=muid)
                serializer = MessageInfoModelSerializer(messageData)
                res_json = {'data': serializer.data, 'msg': 'ok', 'code': 1}
            except MessageInfo.DoesNotExist:
                res_json = {'data': '', 'msg': 'ok', 'code': -1}
        # 没有消息
        else:
            res_json = {'data': '', 'msg': 'ok', 'code': 0}
        return Response(res_json)

    @method_decorator(my_token.logging_check)
    def getAllMessage(self, request):
        user = request.user
        uid = user.uid
        try:
            messageData = MessageInfo.objects.filter(uid=uid)
            serializer = MessageInfoModelSerializer(messageData, many=True)
            res_json = {'data': serializer.data, 'msg': 'ok', 'code': 1}
        except MessageInfo.DoesNotExist:
            res_json = {'data': '', 'msg': 'ok', 'code': -1}

        return Response(res_json)