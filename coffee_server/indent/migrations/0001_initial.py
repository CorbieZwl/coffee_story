# Generated by Django 2.2.12 on 2020-10-21 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0004_auto_20201010_1944'),
        ('goods', '0003_auto_20201003_1351'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndentInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Inum', models.CharField(max_length=64, verbose_name='商品编号')),
                ('info', models.TextField(verbose_name='订单信息')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('goods_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsInfo', verbose_name='商品')),
                ('user_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserInfo', verbose_name='用户')),
            ],
        ),
    ]
