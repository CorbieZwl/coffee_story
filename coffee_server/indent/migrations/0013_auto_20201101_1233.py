# Generated by Django 2.2.12 on 2020-11-01 12:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indent', '0012_auto_20201026_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indentinfo',
            name='timeout',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 2, 12, 33, 58, 542210), verbose_name='过期时间'),
        ),
        migrations.AlterField(
            model_name='yizhif_indent',
            name='Inum',
            field=models.CharField(max_length=64, verbose_name='订单编号'),
        ),
    ]