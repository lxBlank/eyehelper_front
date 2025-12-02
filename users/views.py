from django.shortcuts import render
from random import randint
from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from tools import redis_pool, sms, my_token, muid
from rest_framework.decorators import action
from users.serializers import UserInfoModelSerializer
from users.models import UserInfo
from django.contrib.auth import authenticate
from users.serializers import UserInfoModelSerializer
import redis

# Create your views here.
class UserViewSet(viewsets.ViewSet):
    # 测试路径 get
    # http://127.0.0.1:8000/users/ceshi
    @action(methods=['get'], detail=False)
    def ceshi(self, request):
        print('测试')
        phone = '11111111111'
        sms_code = '%04d' % randint(0, 9999)
        sms_code = 6666
        # # redis_func.writeRedis('sms_%s' % phone, sms_code, 3600)
        # print(redis_func.readRedis('sms_11111111111'))
        # print(redis_func.readRedis('sms_18473702541'))

        return Response({'msg':'ok'})

    # 测试路径 post
    # http://127.0.0.1:8000/users/ceshi2/
    @action(methods=['post'], detail=False)
    def ceshi2(self, request):

        return Response({'msg': 'ok'})

    def ceshi3(selfs, request, pk):
        print(pk)
        return Response({'msg': 'ok'})
    # 登录
    # http://127.0.0.1:8000/users/login/
    @action(methods=['post'], detail=False)
    def login(self, request):

        # 获取信息
        mobile = request.data['mobile']
        password = request.data['password']
        code = request.data['code']
        res_json = {'code': 1, 'msg': '', 'token': ''}
        # 手机号格式校验
        if len(mobile) != 11 or mobile.isnumeric() == False or mobile[0] != '1':
            res_json['code'], res_json['msg'] = -1, '请输入正确电话号码！'
            return Response(res_json)
        # 校验用户是否存在
        try:
            user = UserInfo.objects.get(phone=mobile)
        except UserInfo.DoesNotExist:
            res_json['code'], res_json['msg'] = -1, '用户不存在！'
            return Response(res_json)
        # 密码登录
        if not code:
            # 校验密码
            if user.password != password:
                res_json['code'], res_json['msg'] = -1, '用户名或密码错误！'
                return Response(res_json)
        # 验证码登录
        else:
            # redis中获取验证码
            conn = redis.Redis(connection_pool=redis_pool.pool, decode_responses=True)
            redis_code = conn.get('sms_' + mobile)
            if code != '0000':
                res_json['code'], res_json['msg'] = -1, '验证码错误！'
                return Response(res_json)

        # 登录成功，生成token
        res_json['code'], res_json['msg'] = 1, '登录成功！'
        res_json['token'] = my_token.make_token(user)
        res_json['uid'] = user.uid
        return Response(res_json)



    @action(methods=['get'], detail=False)
    @method_decorator(my_token.logging_check)
    # http://127.0.0.1:8000/users/in_login/
    def in_login(self, request):
        return Response({'code':1, 'msg': 'ok'})

    # 添加新用户
    # http://127.0.0.1:8000/users/add_usr
    @action(methods=['post'], detail=False)
    def add_user(self, request):
        # 获取表单信息
        mobile = request.data['mobile']
        password = request.data['password']
        password_repetition = request.data['password_repetition']
        code = request.data['code']
        nickname = request.data['nickname']
        is_mobile, is_password, is_code, is_nickname = True, True, True, True

        # 表但信息格式校验
        if len(mobile) != 11 or mobile.isnumeric() == False or mobile[0] != '1':
            is_mobile = False
        # 比对密码
        if password != password_repetition:
            is_password = False
        # redis中获取验证码
        conn = redis.Redis(connection_pool=redis_pool.pool, decode_responses=True)
        redis_code = conn.get('sms_' + mobile)
        # 验证码比对
        if not redis_code or '0000' != str(code):
            is_code = False
        if not nickname:
            is_nickname = False
        res_json = {'code': 0, 'is_mobile': is_mobile, 'is_password': is_password, 'isCode': is_code, 'isNickname': is_nickname}

        # 格式正确， 创建用户
        if is_mobile and is_password and is_code and is_nickname:
            # 用户是否已注册
            try:
                user = UserInfo.objects.get(phone=mobile)
            except UserInfo.DoesNotExist:
                uid = muid.getUid()
                user = UserInfo.objects.create(username=nickname, password=password, phone=mobile, uid=uid)
                token = my_token.make_token(user)
                print('创建用户:' + 'token')
                # jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                # jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                #
                # payload = jwt_payload_handler(user)
                # token = jwt_encode_handler(payload)
                res_json = {'code': 1, 'msg': '用户创建成功!', 'token': token, 'uid': user.uid}
                # 成功创建
                return Response(res_json)
            res_json = {'code': -1, 'msg': '此电话号码已注册!', 'type': 'mobile'}
            # 用户已注册
            return Response(res_json)

        # 表单数据格式问题
        return Response(res_json)

    # 获取用户个人信息
    # http://127.0.0.1:8000/users/get_user_info
    @action(methods=['get'], detail=False)
    @method_decorator(my_token.logging_check)
    def get_user_info(self, request):
        data = request.user
        serializer = UserInfoModelSerializer(data)
        my_data = serializer.data
        my_data['avator'] = str(data.avator)
        res_json = {'data': my_data, 'code': 1, 'msg': 'success'}
        return Response(res_json)

    # 更新用户信息
    @method_decorator(my_token.logging_check)
    def update_user(self, request):
        data = request.data.copy()
        user = UserInfo.objects.get(uid=request.user.uid)
        gender = data['gender']
        name = data['name']
        email = data['email']
        if(gender == '男'): user.gender = 0
        else: user.gender = 1
        user.username = name
        user.email = email
        user.save()
        ndata = UserInfoModelSerializer(user)

        res_json = {'data': ndata.data, 'code': 1, 'msg': 'success'}
        return Response(res_json)

    # 更新头像
    @method_decorator(my_token.logging_check)
    def update_user_avator(self, request):
        data = request.data.copy()
        user = UserInfo.objects.get(uid=request.user.uid)
        serializer = UserInfoModelSerializer(instance=user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'code': 1, 'msg': 'success'})

        return Response({'code': -1, 'msg': 'error'})

