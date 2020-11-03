from django.http import JsonResponse
from django.shortcuts import render
import json
import hashlib
from user.models import UserInfo
from tools import token_tools
from django.views import View


# Create your views here.

class UstokenView(View):




    # 登陆
    def post(self,request):
        # 判断请求类型是否为post
        if request.method != "POST":
            result = {"code": "10070", "error": "request is wrong"}
            return JsonResponse(result)
        # 数据反序列化
        json_str = request.body
        json_obj = json.loads(json_str)
        email = json_obj["email"]
        password = json_obj["password"]

        # 判断数据是否为空
        if not email or not password:
            result = {"code": "10071", "error": "email or password is wrong"}
            return JsonResponse(result)
        # 根据email字段查询对象 对比密码是否正确
        try:
            user = UserInfo.objects.get(email=email)
        except Exception as e:
            result = {"code": "10072", "error": "password or email is wrong"}
            return JsonResponse(result)
        else:
            s = hashlib.sha256()
            s.update(password.encode())
            password_h = s.hexdigest()
            # 判断密码是否一致
            if password_h != user.password:
                result = {"code": "10074", "error": "密码错误"}
                return JsonResponse(result)
            else:
                # 密码正确 签发token
                user_id = user.id
                token = token_tools.make_token(user_id).decode()
                result = {"code": 200, "data": {"token": token, "userId": user_id}}
                return JsonResponse(result)
