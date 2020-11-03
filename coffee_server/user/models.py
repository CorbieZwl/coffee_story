from django.db import models

# Create your models here.

class UserInfo(models.Model):
    # 邮箱
    email = models.EmailField('邮箱',null=False, unique=True)
    # 昵称
    nickname = models.CharField('昵称',max_length=32)
    # 地址 省
    address = models.CharField('地址select',max_length=32)
    # 市
    city = models.CharField('地址select', max_length=32,default='')
    # 密码 sha256
    password = models.CharField('密码',max_length=64)
    # 详细地址
    detailed_address = models.TextField('详细地址/text')
    # 是否具有管理员权限 // 待用  存入True False
    administrator = models.BooleanField(default=False)
    def __str__(self):
        return self.nickname

    # 数据表重命名
    class Meta:
        db_table = "user_user_info"
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
