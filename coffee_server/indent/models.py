from django.db import models
from user.models import UserInfo
from goods.models import GoodsInfo
import datetime


# Create your models here.
# 未支付订单
class IndentInfo(models.Model):
    """订单编号不同于订单序列号 订单序列号为自动生成的每一条记录的ID 订单编号为一整个订单的编号"""
    """订单编号 = 'cs'+时间戳(精确到秒)+用户ID"""
    Inum = models.CharField('订单编号', max_length=64)
    user_info = models.ForeignKey(UserInfo, verbose_name='用户', on_delete=models.CASCADE)
    goods_info = models.ForeignKey(GoodsInfo, verbose_name='商品', on_delete=models.CASCADE)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    # 0 未付款  1 已付款 废弃
    timeout = models.DateTimeField('过期时间', default=datetime.datetime.now() + datetime.timedelta(days=1))
    info = models.TextField('订单信息',default='')


# 已支付订单
class Yizhif_indent(models.Model):
    """订单编号不同于订单序列号 订单序列号为自动生成的每一条记录的ID 订单编号为一整个订单的编号"""
    """订单编号 = 'cs'+时间戳(精确到秒)+用户ID"""
    Inum = models.CharField('订单编号', max_length=64)
    user_info = models.ForeignKey(UserInfo, verbose_name='用户', on_delete=models.CASCADE)
    # goods_info = models.ForeignKey(GoodsInfo, verbose_name='商品', on_delete=models.CASCADE)
    info = models.TextField('订单信息')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    # 0 未付款  1 已付款 废弃

# 订单编号 用户 映射
class Indent_User(models.Model):
    user_info = models.ForeignKey(UserInfo, verbose_name='用户', on_delete=models.CASCADE)
    Inum = models.CharField('订单编号', max_length=64)
    zhuangt = models.CharField('支付状态',max_length=8,default='0')