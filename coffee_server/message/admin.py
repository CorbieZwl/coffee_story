from django.contrib import admin
from .models import Messages
# Register your models here.
class MessagesManager(admin.ModelAdmin):
    # 显示字段信息
    list_display = ["id", "user_info", "goods_info", "content", "created_time"]

    # 设置带有超链接的字段
    list_display_links = ['id']
    # 设置右侧过滤器
    # list_filter = ['brand']
    # 条件搜索
    # search_fields = ['name']
    # 可以直接在列表中编辑
    # list_editable = ['temperature']


admin.site.register(Messages, MessagesManager)
