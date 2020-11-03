from django.contrib import admin
from .models import UserInfo


# Register your models here.


class UserInfoManager(admin.ModelAdmin):
    # 显示字段信息
    list_display = ["id", "email", "nickname", "address", "password", "detailed_address", "administrator"]

    # 设置带有超链接的字段
    list_display_links = ['email', 'id']
    # 设置右侧过滤器
    # list_filter = ['brand']
    # 条件搜索
    # search_fields = ['name']
    # 可以直接在列表中编辑
    # list_editable = ['temperature']


admin.site.register(UserInfo, UserInfoManager)
