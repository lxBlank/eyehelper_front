# Websocket 路由
from django.urls import path, include, re_path
from . import consumer

websocket_urlpatterns = {
    # 服务器端向客户端主动推送消息路由
    re_path(r'ws/task/(?P<uid>\w+)/$', consumer.taskConsumer.as_asgi()),
}