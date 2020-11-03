# Generated by Django 2.2.12 on 2020-10-26 19:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indent', '0010_auto_20201026_0023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='yizhif_indent',
            name='goods_info',
        ),
        migrations.AddField(
            model_name='indent_user',
            name='zhuangt',
            field=models.CharField(default='0', max_length=8, verbose_name='支付状态'),
        ),
        migrations.AlterField(
            model_name='indentinfo',
            name='timeout',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 27, 19, 12, 0, 511422), verbose_name='过期时间'),
        ),
    ]