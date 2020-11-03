from django.db import models
from goods.models import GoodsInfo
from user.models import UserInfo


# Create your models here.

class CartInfo(models.Model):
    # 关联商品
    goods_info = models.ForeignKey(GoodsInfo,verbose_name="商品", on_delete=models.CASCADE)
    # 关联用户
    user_info = models.ForeignKey(UserInfo,on_delete=models.CASCADE)
    # 数量 最大为9
    number = models.IntegerField()

