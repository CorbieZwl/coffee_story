# Generated by Django 2.2.12 on 2020-10-21 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indent', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='indentinfo',
            name='state',
            field=models.CharField(default='0', max_length=8, verbose_name='订单状态'),
        ),
    ]
