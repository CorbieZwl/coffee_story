import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View

from coffee_server import settings
from user.models import UserInfo
from goods.models import GoodsInfo
from .models import Favorite_info
from django.utils.decorators import method_decorator
from tools.token_tools import login_check


# Create your views here.
class FavoriteViews(View):

    @method_decorator(login_check)
    def get(self, request, user_id):
        try:
            user = UserInfo.objects.get(id=user_id)
        except Exception as e:
            print('Error is %s' % e)
            result = {'code': 1001, 'error': 'the user_id is error'}
            return JsonResponse(result)
        try:
            FCoffee = Favorite_info.objects.filter(user_info_id=user_id)
        except Exception as e:
            print('Error is %s' % e)
            result = {'code': 1002, 'error': 'the user_id is error'}
            return JsonResponse(result)
        res = {'code': 200, 'data': []}
        print(FCoffee)
        for F in FCoffee:
            f_dict = {}
            f_dict['name'] = F.goods_name
            f_dict['id'] = F.id
            f_dict['price'] = F.goods_price
            a = GoodsInfo.objects.get(id=int(F.goods_id)).imgurl
            imgurl = a.replace('127.0.0.1', settings.IP_str)
            f_dict['imgurl'] = imgurl
            f_dict['inventory'] = GoodsInfo.objects.get(id=int(F.goods_id)).inventory
            f_dict['goods_id']=F.goods_id
            res['data'].append(f_dict)
        return JsonResponse(res)

    def delete(self, request, user_id, delete_id):
        try:
            coffee = Favorite_info.objects.get(user_info_id=user_id, id=delete_id)
        except Exception as e:
            print('Error is %s' % e)
            result = {'code': 1003, 'error': 'the goods_info is error'}
            return JsonResponse(result)
        try:
            coffee.delete()
        except Exception as e:
            print('Error is %s' % e)
            result = {'code': 1003, 'error': 'deletion is unsuccessful'}
            return JsonResponse(result)
        return JsonResponse({'code': 200})

    # 判断登陆状态
    @method_decorator(login_check)
    def post(self, request, user_id):
        try:
            user = UserInfo.objects.get(id=user_id)
        except Exception as e:
            print('Error is %s' % e)
            result = {'code': 1001, 'error': 'the user_id is error'}
            return JsonResponse(result)
        json_str = request.body
        json_obj = json.loads(json_str)
        goods_id = json_obj['goods_id']
        try:
            coffee = GoodsInfo.objects.get(id=int(goods_id))
        except Exception as e:
            print('Error is %s' % e)
            result = {'code': 1001, 'error': 'the goods_id is error'}
            return JsonResponse(result)
        name = coffee.name
        price = coffee.price
        goods_id = str(coffee.id)
        user_id = user_id
        # 检查goods是否已经存在于收藏夹
        old_goods = Favorite_info.objects.filter(goods_id=int(goods_id))
        if old_goods:
            result = {'code': 1002, 'error': '已存在收藏夹'}
            return JsonResponse(result)
        try:
            Favorite_info.objects.create(goods_id=int(goods_id), goods_name=name, goods_price=price,
                                         user_info_id=int(user_id))
        except Exception as e:
            print('Error is %s' % e)
            result = {'code': 1003, 'error': 'add_goods_info is error'}
            return JsonResponse(result)
        return JsonResponse({'code': 200})
