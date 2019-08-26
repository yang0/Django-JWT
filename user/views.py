from django.contrib.auth.backends import ModelBackend
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
from rest_framework_jwt.utils import jwt_decode_handler

from user.models import AgentOrSaleManOrOperate


class CustomBackend(ModelBackend):
    """
    自定义用户验证规则
    """
    def authenticate(self, mobile=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因
            # 后期可以添加邮箱验证
            user = AgentOrSaleManOrOperate.objects.get(mobile=mobile)
            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self,
            # raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class Agent(APIView):
    """代理商详情"""
    permission_classes = [ ]
    def get(self, request, *args, **kwargs):
        user = request.user
        print(user.id)

        return Response('ok', status=status.HTTP_200_OK)

