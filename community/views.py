from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.response import Response
from tools import audioex

# Create your views here.
class CommunityViewSet(viewsets.ViewSet):
    def getAudio(self, request):
        mtext = '未查到'
        if 'text' in request.data:
            mtext = request.data['text']
        url = audioex.getAudio(mtext)
        # url = 'http://127.0.0.1:8000/media/audio/ceshi.mp3'
        res_json = {'data': url, 'msg': 'ok', 'code': 1}
        return Response(res_json)