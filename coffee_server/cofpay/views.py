from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
# 需要安装阿里pay模块
from alipay import AliPay
from django.views import View
from django.conf import settings
import json


# Create your views here.

# 试用
app_private_key_string = open(settings.ALIPAY_KEY_DIR+"app_private_key.pem").read()
alipay_public_key_string = open(settings.ALIPAY_KEY_DIR+"alipay_public_key.pem").read()
ORDER_STATUS = 1  # 记录支付状态 1-待支付  2-支付成功 3-支付失败
# 1.基类(创建AliPay对象,封装api)
class MyAliPay(View):
    # **kwargs是为了调用关键字传参
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.alipay = AliPay(
            appid=settings.ALIPAY_APP_ID,
            #  当前app的私钥(对请求签名)
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥 验签
            alipay_public_key_string=alipay_public_key_string,
            # 签名算法(RSA SHA2)
            sign_type='RSA2',
            # 指明是测试模式
            debug=True,
            app_notify_url=None
        )

    def get_trade_url(self,order_id,amount):
        base_url = 'https://openapi.alipaydev.com/gateway.do'
        # 订单信息
        order_string = self.alipay.api_alipay_trade_page_pay(
            # 订单编号
            out_trade_no=order_id,
            total_amount=amount,
            # 订单标题
            subject='强无敌强无敌强无敌强无敌强无敌强无敌强无敌强无敌强无敌',
            return_url=settings.ALIPAY_RETURN_URL,
            notify_url=settings.ALIPAY_NOTIFY_URL
        )
        return base_url+'?'+order_string

    # 验证函数
    def get_verify_result(self,data,sign):
        # True: 验证通过  False:失败 验证请求是否出自阿里
        return self.alipay.verify(data,sign)

    # 查询函数 找支付宝服务器要结果
    def get_trade_result(self,order_id):
        result = self.alipay.api_alipay_trade_query(out_trade_no=order_id)
        # 获取交易状态 并判断是否通过
        if result.get('trade_status') == 'TRADE_SUCCESS':
            return True
        return False

class JumpView(MyAliPay):
    def get(self,request):
        return render(request,'ajax_alipay.html')

    def post(self,request,user_id=None):
        print('-------------------')
        json_obj = json.loads(request.body)
        order_id = json_obj['order_id']
        jine = json_obj['jine']
        pay_url = self.get_trade_url(order_id,jine)
        return JsonResponse({"pay_url":pay_url})


class ResultView(MyAliPay):
    def get(self,request):
        # 支付过程完成
        request_data = {k: request.GET[k] for k in request.GET.keys()}
        print(request_data)
        order_id = request_data['out_trade_no']
        if ORDER_STATUS ==2:
            return HttpResponse('<h1>诶 很舒服</h1>')
        elif ORDER_STATUS ==1:
            result = self.get_trade_result(order_id)
            if result:
                return HttpResponse("<h1>诶 就很舒服</h1>")
            else:
                return HttpResponse("<h1>哟 多捞哦</h1>")


    def post(self,request):
        # 支付完毕后 支付宝发送post请求  告知结果
        # 拿到支付结果 如果成功 修改订单状态为已付款
        # 否则 设置订单状态为支付失败
        # 将类字典结构改为字典结构 因为需要使用字典结构
        request_data = {k:request.POST[k] for k in request.POST.keys()}
        # 从字典格式的数据中 取出签名
        sign = request_data.pop('sign')
        is_verify = self.get_verify_result(request_data,sign)
        if is_verify:
            trade_status = request_data['trade_staus']
            if trade_status == 'TRADE_SUCCESS':
                # 在数据库中 将订单状态由待支付修改为已支付
                # ORDER_STATUS = 2
                return HttpResponse('ok')
            else:
                # 在数据库中将订单数据由待支付修改为支付失败
                # ORDER_STATUS = 2
                return HttpResponse('ok')
        else:
            return HttpResponse('非法访问')
