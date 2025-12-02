from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class MessageInfo(models.Model):
    # muid
    muid = models.CharField(max_length=50, default='')
    # uid
    uid = models.CharField(max_length=50, default='')
    # 内容
    content = models.CharField(max_length=100, default='')
    # 时间
    timestamp = models.CharField(max_length=20, default='')
