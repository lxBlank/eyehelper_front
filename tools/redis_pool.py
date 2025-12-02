#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2022/11/26 9:58
# @Author  : liuxin
# @File    : redis_pool.py
# @Software: PyCharm
import redis
# 创建连接池
pool = redis.ConnectionPool(host='localhost', port=6379, db=5, max_connections=1000)
