from django.shortcuts import render
import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from coffee_server import settings
from tools.token_tools import login_check
from user.models import UserInfo
from goods.models import GoodsInfo
from .models import CartInfo
# Create your views here.

class CartViews(View):
    @method_decorator(login_check)
    def get(self,request,user_id=None):
        print(user_id)
        try:
            user = UserInfo.objects.get(id=user_id)
            print(1)
        except Exception as e:
            print('Error is %s' % e)
            result = {'code': 1001, 'error': 'the user_id is error'}
            return JsonResponse(result)
        try:
            CCoffee = CartInfo.objects.filter(user_info_id=user_id)
        except Exception as e:
            print('Error is %s' % e)
            result = {'code': 1002, 'error': 'the user_id is error'}
            return JsonResponse(result)
        res = {'code': 200, 'data': []}
        for C in CCoffee:
            c_dict={}
            c_dict['id']=C.goods_info.id
            # c_dict['number']=C.number
            c_dict['name']=GoodsInfo.objects.get(id=int(C.goods_info_id)).name
            a =GoodsInfo.objects.get(id=int(C.goods_info_id)).imgurl
            imgurl = a.replace('127.0.0.1', settings.IP_str)
            c_dict['imgurl'] = imgurl
            c_dict['price'] = GoodsInfo.objects.get(id=int(C.goods_info_id)).price
            c_dict['number']=C.number
            res['data'].append(c_dict)
        print(res)
        return JsonResponse(res)

    @method_decorator(login_check)
    def post(self,request,user_id=None):
        print(user_id)
        try:
            user=UserInfo.objects.get(id=user_id)
        except Exception as e:
            print('Error is %s'%e)
            result={'code':1001,'error':'the user_id is error'}
            return JsonResponse(result)
        json_str=request.body
        json_obj=json.loads(json_str)
        goods_id=json_obj['goods_id']
        try:
            coffee=GoodsInfo.objects.get(id=int(goods_id))
        except Exception as e:
            print('Error is %s'%e)
            result={'code':1001,'error':'the goods_id is error'}
            return JsonResponse(result)
        goods_info_id=goods_id
        user_info_id=user_id
        #检查购物车是否已存在此商品
        old_goods = CartInfo.objects.filter(goods_info_id=int(goods_id))
        if old_goods:
            result = {'code': 1002, 'error':'购物车中已存在此商品'}
            return JsonResponse(result)
        try:
            CartInfo.objects.create(goods_info_id=int(goods_info_id),user_info_id=int(user_info_id),number=1)
        except Exception as e:
            print('Error is %s'%e)
            result={'code':1003,'error':'add_goods_info is error'}
            return JsonResponse(result)
        return JsonResponse({'code': 200})

    @method_decorator(login_check)
    def delete(self,request,user_id,delete_id):
        try:
            coffee=CartInfo.objects.get(user_info_id=user_id,goods_info_id=delete_id)
        except Exception as e:
            print('Error1 is %s'%e)
            result={'code':1003,'error':'the goods_info is error'}
            return JsonResponse(result)
        try:
            coffee.delete()
        except Exception as e:
            print('Error2 is %s'%e)
            result={'code':1003,'error':'deletion is unsuccessful'}
            return JsonResponse(result)
        return JsonResponse({'code':200})
    def put(self,request,user_id,num,cart_goods_id):
        try:
            coffee=CartInfo.objects.get(user_info_id=user_id,goods_info_id=cart_goods_id)
        except Exception as e:
            print('Error1 is %s'%e)
            result={'code':1003,'error':'the user_info is error'}
            return JsonResponse(result)
        try:
            num=int(num)
        except Exception as e:
            print('Error2 is %s'%e)
            result={'code':200,'data':'请输入数量(1~9)'}
            return JsonResponse(result)
        if 0<=int(num)<=9:
            try:
                coffee.number=int(num)
                coffee.save()
            except Exception as e:
                print('Error3 is %s' % e)
                result = {'code': 1004, 'error': 'number_save is unsuccessful'}
                return JsonResponse(result)
            return JsonResponse({'code':200,'data':''})
        else:
            return JsonResponse({'code':200,'data':'咖啡的数量最大为9,请输入数量(1~9)'})

