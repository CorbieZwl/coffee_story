from django.contrib import admin
from .models import IndentInfo
from .models import Indent_User
from .models import Yizhif_indent


# Register your models here.

class IndentInfoManager(admin.ModelAdmin):
    # 显示字段信息
    list_display = ["Inum", "user_info", "goods_info", "create_time"]

    # 设置带有超链接的字段
    list_display_links = ['Inum']


admin.site.register(IndentInfo,IndentInfoManager)





admin.site.register(Indent_User)
admin.site.register(Yizhif_indent)
