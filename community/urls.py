#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2022/11/28 21:24
# @Author  : liuxin
# @File    : urls.py
# @Software: PyCharm

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from community import views



urlpatterns = [
    path('audio/', views.CommunityViewSet.as_view({'post': 'getAudio'})),
]