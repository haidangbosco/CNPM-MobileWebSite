# Generated by Django 2.0.4 on 2018-05-21 17:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobile_sale_app', '0003_auto_20180521_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 22, 0, 31, 16, 471658)),
        ),
        migrations.AlterField(
            model_name='order',
            name='time_order',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 22, 0, 31, 16, 470658), editable=False),
        ),
    ]