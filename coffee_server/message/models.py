from django.db import models
from user.models import UserInfo
from goods.models import GoodsInfo

# Create your models here.

class Messages(models.Model):
    # 关联用户
    user_info = models.ForeignKey(UserInfo,on_delete=models.CASCADE)
    # 关联商品
    goods_info = models.ForeignKey(GoodsInfo,on_delete=models.CASCADE)
    # 创建时间 默认为添加时间
    created_time = models.DateTimeField(auto_now_add=True)
    # 评论内容
    content = models.CharField(max_length=256)

