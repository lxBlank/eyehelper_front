#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2022/11/16 14:20
# @Author  : liuxin
# @File    : my_token.py
# @Software: PyCharm
#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2022/11/16 14:02
# @Author  : liuxin
# @File    : jwt.py
# @Software: PyCharm
from django.http import JsonResponse
from users.models import UserInfo
from eye_backend import settings
from users.serializers import UserInfoModelSerializer
import time
import jwt

# 生成Token
def make_token(user, expire=3600 * 24, algorithm='HS256'):
    """
    :param user: 对象
    :param expire: 过期时间
    :param algorithm: 加密算法
    :return:
    """
    key = settings.SECRET_KEY
    now_t = time.time()
    payload_data = {'uid': user.uid, 'username': user.username,  'ext': now_t + expire}
    print(payload_data)
    return jwt.encode(payload_data, key, algorithm)

# 登录装饰器
def logging_check(func):
    def wrap(request, *args, **kwargs):
        # 获取token
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            result = {'code': -6, 'msg': 'Please login'}
            return JsonResponse(result)
        # 校验jwt
        try:
            res = jwt.decode(token, settings.SECRET_KEY)
        except Exception as e:
            result = {'code': -7, 'msg': 'Please login'}
            print('jwt decode error is %s' %(e))
            return JsonResponse(result)
        # 校验是否过期
        now_t = time.time()
        if now_t > res['ext']:
            result = {'code': -8, 'msg': 'Please login'}
            return JsonResponse(result)
        # 获取登录用户
        uid = res['uid']
        user = UserInfo.objects.get(uid=uid)
        request.user = user

        return func(request, *args, **kwargs)
    return wrap

