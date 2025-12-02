from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserInfo(models.Model):
    # uid
    uid = models.CharField(max_length=50, default='')
    # 用户名
    username = models.CharField(max_length=20, default='')
    # 密码
    password = models.CharField(max_length=20, default='')
    # 手机号
    phone = models.CharField(max_length=11, default='')
    # 性别    0:男    1:女
    gender = models.IntegerField(default=0)
    # 是否激活  0:未激活  1:激活
    isActive = models.IntegerField(default=1)
    # 角色    0:普通角色  1:管理员
    role = models.IntegerField(default=0)
    # 权限
    primission = models.IntegerField(default=0)
    # 头像
    avator = models.ImageField(upload_to='avator', default='static/avator/default.png')
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 更新时间
    update_time = models.DateTimeField(auto_now=True)