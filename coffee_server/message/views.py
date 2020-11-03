from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from goods.models import GoodsInfo
from user.models import UserInfo
from .models import Messages
import json
from tools.token_tools import login_check


# Create your views here.
# 接收评论 存入数据库
@login_check
def view_messages(request, goods_id):
    if request.method != "POST":
        result = {"code": "10050", "error": "request is error"}
        return JsonResponse(result)
    json_str = request.body
    json_obj = json.loads(json_str)
    content = json_obj.get("content")
    # 判断评论内容是否为空
    if not content:
        result = {"code": "10052", "error": "不能发表空白评论"}
        return JsonResponse(result)
    user_id = json_obj.get("user_id")
    # 判断用户和商品是否存在
    try:
        goods_obj = GoodsInfo.objects.get(id=goods_id)
        user_obj = UserInfo.objects.get(id=user_id)
    except Exception as e:
        print(e)
        result = {"code": "10051", "error": "data is error"}
        return JsonResponse(result)
    else:
        Messages.objects.create(goods_info=goods_obj, user_info=user_obj, content=content)

        return JsonResponse({"code": 200})
