#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2022/11/15 22:01
# @Author  : liuxin
# @File    : urls.py
# @Software: PyCharm

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users import views

router = DefaultRouter()
router.register(r'', views.UserViewSet, basename="users")

urlpatterns = [
    path('', include(router.urls)),
    path('ceshi3/<int:pk>', views.UserViewSet.as_view({'get': 'ceshi3'})),
    path('update/info/', views.UserViewSet.as_view({'post': 'update_user'})),
    path('update/avator/', views.UserViewSet.as_view({'post': 'update_user_avator'}))
]