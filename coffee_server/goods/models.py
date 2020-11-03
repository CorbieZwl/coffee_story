from django.db import models


# Create your models here.

class GoodsInfo(models.Model):
    # 商品名
    name = models.CharField("商品名",max_length=32, null=False)
    # 数量
    num = models.IntegerField('数量',default=100)
    # 单价
    price = models.DecimalField("单价",max_digits=7, decimal_places=2, null=False)
    # 温度 [cold ,hot]
    temperature = models.CharField("温度",max_length=16)
    # 品牌
    brand = models.CharField("品牌",max_length=16)
    # 订单数
    indent_num = models.IntegerField("订单数")
    # 库存
    inventory = models.IntegerField("库存")
    # 评分
    score = models.DecimalField("评分",max_digits=2, decimal_places=1, default=5)
    # 评分人数
    pnumber = models.IntegerField("评分人数",default=0)
    # 备注
    remark = models.TextField("备注")
    #
    imgurl = models.URLField(default="http://127.0.0.1:8000/static/6.png")
    def __str__(self):
        return self.name

    # 重命名
    class Meta:
        db_table = "goods_goods_info"
        verbose_name = "商品信息"
        verbose_name_plural = verbose_name