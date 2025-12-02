# Websocket 视图
from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

# 服务端向客户端主动推送
class taskConsumer(WebsocketConsumer):
    """
    同步患者端和家属端事务卡片
    向各家属端推送患者摔倒消息
    """

    # 建立连接
    def websocket_connect(self, message):
        # 获取路由中的uid
        uid = self.scope['url_route']['kwargs'].get('uid')
        # 服务端允许客户端建立连接
        self.accept()
        async_to_sync(self.channel_layer.group_add)(uid, self.channel_name)

    # 接收和转发消息
    def websocket_receive(self, message):
        # 获取路由中的uid
        uid = self.scope['url_route']['kwargs'].get('uid')
        async_to_sync(self.channel_layer.group_send)(uid, {'type': 'tt.kk', 'message': message})

    def tt_kk(self, event):
        text = event['message']['text']
        self.send(text)

    # 客户端与服务器断开连接
    def websocket_disconnect(self, message):
        raise StopConsumer()


class tripConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        # 获取路由中的uid
        uid = self.scope['url_route']['kwargs'].get('uid')
        print('建立连接！')
        # 服务端允许客户端建立连接
        self.accept()
        async_to_sync(self.channel_layer.group_add)(uid, self.channel_name)

    def websocket_receive(self, message):
        # 获取路由中的uid
        uid = self.scope['url_route']['kwargs'].get('uid')
        async_to_sync(self.channel_layer.group_send)(uid, {'type': 'xx.oo', 'message': message})

    def xx_oo(self, event):
        text = event['message']['text']
        self.send(text)

    def websocket_disconnect(self, message):
        # 客户端与服务器断开连接
        raise StopConsumer()