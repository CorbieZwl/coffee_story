from django.contrib import admin
from .models import GoodsInfo


# Register your models here.


class GoodsInfoManager(admin.ModelAdmin):
    # 显示字段信息
    list_display = ["id","name","price",'num',"temperature","brand","indent_num","inventory","score","pnumber","remark"]

    # 设置带有超链接的字段
    list_display_links = ['name', 'id']
    # 设置右侧过滤器
    list_filter = ['brand']
    # 条件搜索
    search_fields = ['name']
    # 可以直接在列表中编辑
    list_editable = ['temperature']

admin.site.register(GoodsInfo, GoodsInfoManager)
