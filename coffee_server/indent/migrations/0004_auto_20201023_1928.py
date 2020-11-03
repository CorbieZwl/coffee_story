# Generated by Django 2.2.12 on 2020-10-23 19:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indent', '0003_remove_indentinfo_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='indentinfo',
            name='state',
            field=models.CharField(default='0', max_length=8, verbose_name='订单状态'),
        ),
        migrations.AddField(
            model_name='indentinfo',
            name='timeout',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 24, 19, 28, 18, 922404), verbose_name='过期时间'),
        ),
    ]
