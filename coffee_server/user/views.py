from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings
from .models import UserInfo
# Create your views here.
from .models import UserInfo
import random
from django.views import View
import re
import hashlib
import jwt
import time
import json
from tools.token_tools import getuser_token, login_check
from django.utils.decorators import method_decorator
from random import randint
from django.core.cache import cache
from .task import send_varcode_email


# 插入用户数据(不要重复)
def adduserinfo(request):
    list01 = ["李赛琳", "找回最初的我", "主杀忠必反", "持枪少女", "大叔不淑", "清子", "有烟有酒有孤独", "雯雯小可爱"]
    list02 = ['佛山', '南宁', '北海', '杭州', '南昌', '厦门', '温州']
    list03 = ["一区", "二区", "三区", "四区", "五区"]
    for i in range(20000, 20020):
        email = str(i) + "@wd.com"
        nickname = random.choice(list01) + str(i)
        address = random.choice(list02)
        password = str(random.randint(100000, 999999))
        detailed_address = address + random.choice(list03)
        try:
            UserInfo.objects.create(
                email=email,
                nickname=nickname,
                address=address,
                password=password,
                detailed_address=detailed_address
            )
        except Exception as e:
            return HttpResponse(f"error is {e}")

    return HttpResponse("插入成功")


def make_token(email, expire=3600 * 24):
    key = settings.JWT_TOKEN_KEY
    now = time.time()
    payload = {'email': email, 'exp': now + expire}
    return jwt.encode(payload, key, algorithm='HS256')


class UserView(View):

    def post(self, request):
        json_str = request.body
        json_obj = json.loads(json_str)
        # 昵称
        nickname = json_obj['nickname']
        # 邮箱
        email = json_obj['email']
        # 验证码
        auth_code = json_obj['authCode']
        # 生成获取验证码的键
        emkey = 'em{}'.format(email)
        # 系统生成验证码
        varcode = cache.get(emkey)
        # 判断验证码是否正确
        if auth_code != varcode:
            return JsonResponse({"code": "92412","error":"验证码错误"})
        # 密码和确认密码
        password_1 = json_obj['password1']
        password_2 = json_obj['password2']
        # 判断是否为空
        if not nickname or not email or not auth_code or not password_2 or not password_1:
            result = {"code": "10060", "error": "输入数据不能为空"}
            return JsonResponse(result)
        # 判断邮箱格式是否正确
        if '*' in email or '@' not in email:
            result = {"code": 10105, 'error': '邮箱输入有误'}
            return JsonResponse(result)

        # 检查邮箱是否可用
        old_email = UserInfo.objects.filter(email=email)
        if old_email:
            result = {'code': 10103, 'error': '此邮箱已被注册'}
            return JsonResponse(result)
        # 检查两次密码是否一致
        if password_1 != password_2:
            result = {'code': 10104, 'error': '两次密码不一致'}
            return JsonResponse(result)
        # 密码 用sha256加密
        s = hashlib.sha256()
        s.update(password_1.encode())
        password_h = s.hexdigest()
        # 插入数据 当并发量高当时候 可能会出现重复
        try:
            user = UserInfo.objects.create(nickname=nickname, password=password_h, email=email)
        except Exception as e:
            print(f'create error is {e}')
            result = {'code': 10103, 'error': '注册失败'}
            return JsonResponse(result)
        else:
            print("ok")
            return JsonResponse({"code": "200"})

        # # 签发token  是否签发
        # token = make_token(email)
        # result = {'code': 200, "data": {'token': token}}
        # return JsonResponse(result)

    @method_decorator(login_check)
    def get(self, request, user_id=None):
        return JsonResponse({"code": "200", "data": {"nickname": request.myuser.nickname}})


# post请求
def create_verification_code(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    # 获取邮箱
    user_email = json_obj['email']
    # 生成缓存的键
    emkey = 'em{}'.format(user_email)
    # 判断本邮箱是否在60s内获取过验证码
    if cache.get(emkey):
        return JsonResponse({"code":"90871","error":"请勿频繁获取验证码"})
    # 生成验证码
    ver_code = str(randint(100000, 999999))
    # 生成缓存的值
    value = ver_code
    # # 存入redis
    cache.set(emkey,value,timeout=63)
    # 调用消费者
    send_varcode_email.delay(user_email,ver_code)
    return JsonResponse({"code": 200})
