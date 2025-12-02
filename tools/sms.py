#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2022/11/15 22:45
# @Author  : liuxin
# @File    : sms.py
# @Software: PyCharm
import datetime
import hashlib
import base64
import requests
import json
from eye_backend import settings

class YunTongXin():
    # 容联云生产环境的base url
    base_url = 'https://app.cloopen.com:8883'
    # 账户ID
    accountSid = settings.ACCOUNT_SID
    # 授权令牌
    accountToken = settings.AUTH_TOKEN

    def __init__(self, APP_ID=settings.APP_ID, template_id=settings.TEMPLATE_ID):
        # 默认应用ID
        self.appId = APP_ID
        # 默认模板ID
        self.templateId = template_id

    # 获取最终拼接业务url
    def get_request_url(self, signature):
        url = '/2013-12-26/Accounts/%s/SMS/TemplateSMS?' \
              'sig=%s' %(self.accountSid, signature)
        self.url = self.base_url + url
        return self.url

    # 生成时间戳
    def get_timestamp(self):
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    # 生成签名
    def get_signature(self, time_stamp):
        s = self.accountSid + self.accountToken + time_stamp
        m = hashlib.md5()
        m.update(s.encode())
        return m.hexdigest().upper()

    # 生成请求头
    def get_request_header(self, time_stamp):
        s = self.accountSid + ':' + time_stamp
        auth = base64.b64encode(s.encode()).decode()
        json_res = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'charset': 'utf-8',
            'Content-Length': '256',
            'Authorization': auth
        }
        return json_res
    # 获得请求体
    def get_request_body(self, code, phone='18463702549', time=3):
        body_dic = {
            'to': phone,
            'appId': self.appId,
            'templateId': self.templateId,
            'datas': [code, time]
        }
        return body_dic

    # 向服务器发送请求
    def request_api(self, url, header, body):
        res = requests.post(url=url, headers=header, data=json.dumps(body))
        return res.text

    # 测试
    def ceshi(self):
        time_stamp = self.get_timestamp()
        signature = self.get_signature(time_stamp)
        url = self.get_request_url(signature)
        print('sms.py-url:'+ url)
        header = self.get_request_header(time_stamp)
        print('sms.py-header:'+ str(header))
        body = self.get_request_body('321222')
        print('sms.py-body:' + str(body))
        res = self.request_api(url, header, body)
        print('sms.py-res:' + str(res))



if __name__ == '__main__':
    obj = YunTongXin()
    obj.ceshi()