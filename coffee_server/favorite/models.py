from django.db import models
from user.models import UserInfo


# Create your models here.

class Favorite_info(models.Model):
    # 商品编号
    goods_id = models.IntegerField()
    # 商品名
    goods_name = models.CharField(max_length=32)
    goods_price = models.DecimalField(max_digits=7, decimal_places=2, null=False,default=19.9)
    # 关联用户
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
