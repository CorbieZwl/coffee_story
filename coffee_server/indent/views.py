from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from goods.models import GoodsInfo
from django_redis import get_redis_connection
from tools.token_tools import login_check
from django.utils.decorators import method_decorator
import json
from django.db.models import F
import time
from .models import IndentInfo, Yizhif_indent
from .models import Indent_User
from datetime import datetime
from cart.models import CartInfo
from .tasks import send_varcode_email

# Create your views here.

class IndentView(View):

    @method_decorator(login_check)
    def get(self, request, user_id=None):
        # 获取该用户所有订单号
        indent_list = Indent_User.objects.filter(user_info=request.myuser)
        # 先获取用户的所有订单号 [(编号,状态),()]
        indent_id_list = []
        for i in indent_list:
            indent_id_list.append((i.Inum, i.zhuangt))
        indent_info_list = self.feedback_indent_info(indent_id_list)
        result = {"code": 200, "data": indent_info_list}
        return JsonResponse(result)

    def feedback_indent_info(self, indent_id_list):
        # print(indent_id_list)
        this_time = datetime.now()
        indent_info_list = []
        # 订单编号	订单信息	创建时间	状态	操作
        for indent in indent_id_list:
            # 查找订单 未支付订单 根据编号 过期时间查询
            # 已支付订单 直接根据编号查找 0 未未支付  1 为已支付
            if indent[1] == "0":
                """未支付"""
                try:
                    ind = IndentInfo.objects.get(Inum=indent[0], timeout__gt=this_time)
                except Exception as e:
                    ind = IndentInfo.objects.filter(Inum=indent[0], timeout__gt=this_time)
                    if ind.count() != 0:
                        indent_info_list.append(
                            {"nid": indent[0], "remark": ind[0].info, "create_time": ind[0].create_time,
                             "zhuangt": "未支付订单,过期时间:{}".format(ind[0].timeout)})

                else:
                    indent_info_list.append({"nid": indent[0], "remark": ind.info, "create_time": ind.create_time,
                                             "zhuangt": "未支付订单,过期时间:{}".format(ind.timeout)})
            elif indent[1] == "1":
                """已支付"""
                try:
                    # print(indent)
                    ind = Yizhif_indent.objects.get(Inum=indent[0])
                except Exception as e:
                    print(2)
                    print(e)
                    continue
                else:
                    indent_info_list.append({"nid": indent[0], "remark": ind.info, "create_time": ind.create_time,
                                             "zhuangt": "已支付"})
        return indent_info_list

    @method_decorator(login_check)
    def post(self, request, user_id=None):
        """检测请求源(商品页或购物车) 调用相关函数"""
        json_obj = json.loads(request.body)
        host = json_obj.get('host')
        print(host)
        if host == 'product':
            # 请求源于商品页
            result = self.product_indent(json_obj['goods'], request.myuser)
        elif host == 'cart':
            # 请求源于购物车
            result = self.cart_indent(json_obj['goods'], request.myuser)
        elif host == 'checkout':
            # 订单已支付 删除未支付订单 创建已支付订单
            result = self.zhifu(json_obj, request.myuser)

        else:
            result = {'code': 60129, 'error': '请求错误'}

        return JsonResponse(result)

    # 创建订单请求 查询商品是否存在 存在且数量足够 生成订单编号 数量减少 存入数据库

    def delete(self,request,user_id=None):
        nid = json.loads(request.body)["nid"]
        try:
            Indent_User.objects.get(Inum=nid).delete()
        except Exception as e:
            print(e)
            result = {"code":24151,"error":"商品错误"}
            return JsonResponse(result)
        result = {"code":200}
        return JsonResponse(result)


    """
    {'host': 'checkout', 'email': '1057926872@qq.com', 
    'seroal': 'ct202010301548527', 'shengs': '2', 'citys': '2', 'juti': '1', 'beizhu': '1'}
    """

    # 获取订单 删除未支付 生成已支付
    def zhifu(self, data, user):
        print(data)
        city_id = data["citys"]
        # 判断城市是否为空
        if city_id == '-1':
            return {"code": 51253, "error": "城市不能为空"}
        email = data['email']
        seroal = data['seroal']
        indents = IndentInfo.objects.filter(Inum=seroal)
        if not indents:
            return {"code": 51251, "error": '订单错误'}
        # 获取订单信息
        remark = indents[0].info
        try:
            indents.delete()
        except:
            return {"code": 21521, "error": "订单生成失败"}

        Yizhif_indent.objects.create(Inum=seroal, user_info=user, info=remark)
        try:
            a = Indent_User.objects.get(Inum=seroal)
            a.zhuangt = '1'
            a.save()
        except:
            return {"code": 23104, "error": "商品错误"}

        send_varcode_email.delay(email,remark)
        return {"code": 200}

    # 商品页直接请求
    def product_indent(self, goods, user):
        """处理商品页发送的创建订单请求"""
        # 遍历修改数据
        gid = goods[0]['goods_id']
        num = int(goods[0]['num'])
        # 商品是否存在
        try:
            tgoods = GoodsInfo.objects.get(id=gid)
        except:
            result = {'code': 89091, "error": '商品有误'}
            return result
        else:
            # 防止高并发修改数据时发生数据混乱 调用F对象
            # .update(num=F('num')-int(goods[0]['num']))
            print(tgoods.num)
            if tgoods.num > num:
                GoodsInfo.objects.filter(id=gid).update(num=F('num') - num)
                # 生成商品编号
                seroal = self.make_serial(user.id)
                # 在mysql中插入订单记录 存入未支付表中 seroal myuser tgoods time.time()+24*3600\
                # 构造数据
                remark = "商品:{}".format(tgoods.name)
                # 插入未支付订单表
                IndentInfo.objects.create(Inum=seroal, user_info=user, goods_info=tgoods, info=remark)
                # 插入映射表 订单编号映射用户
                Indent_User.objects.create(user_info=user, Inum=seroal)
                # 构造响应数据
                result = {"code": "200", "seroal": seroal, "all_total": tgoods.price * num,
                          "goods": [{"name": tgoods.name, "num": num, "total": tgoods.price * num}],
                          "user_info": {"email": user.email, "sheng": user.address, "city": user.city,
                                        "detailed_address": user.detailed_address}}
            else:
                result = {"code": 200, "error": "商品数量不足"}
            return result

    def make_serial(self, user_id):
        tnow = time.localtime(time.time())
        seroal = 'ct' + str(tnow.tm_year) + str(tnow.tm_mon) + str(tnow.tm_mday) + str(tnow.tm_hour) + str(
            tnow.tm_min) + str(tnow.tm_sec) + str(user_id)
        return seroal

    # 购物车请求
    def cart_indent(self, goods, user):
        """处理购物车页发送的创建订单请求 删除购物车数据"""
        goods_id = [i["goods_id"] for i in goods]
        # 商品是否存在
        goods_list = GoodsInfo.objects.filter(id__in=goods_id)
        if goods_list.count() != len(goods_id):
            result = {"code": 92103, "error": "部分商品数量不够"}
            return result
        # 减少商品 增加购物车数据
        goods_info_list = []
        goods_total = 0
        for g in goods:
            num = int(g["num"])
            tgoods = GoodsInfo.objects.filter(id=g["goods_id"])
            tgoods.update(num=F('num') - num)
            print(tgoods)
            goods_info_list.append({"name": tgoods[0].name, "num": num, "total": tgoods[0].price * num})
            goods_total += num * tgoods[0].price
        # 构造订单编号
        seroal = self.make_serial(user.id)
        # 构造商品信息
        remark = "商品:{}".format(','.join([i.name for i in goods_list]))
        # 存入映射表
        Indent_User.objects.create(user_info=user, Inum=seroal)
        # 存入未支付订单表
        for g in goods_list:
            IndentInfo.objects.create(Inum=seroal, user_info=user, goods_info=g, info=remark)
        # 删除购物车数据
        CartInfo.objects.filter(user_info=user).delete()
        # 构造响应
        result = {"code": "200", "seroal": seroal, "all_total": goods_total,
                  "goods": goods_info_list,
                  "user_info": {"email": user.email, "sheng": user.address, "city": user.city,
                                "detailed_address": user.detailed_address}}
        return result
