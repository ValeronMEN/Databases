# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-15 10:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guitarsapp', '0002_auto_20171215_0124'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bill',
            old_name='bill_customer_id',
            new_name='bill_customer',
        ),
        migrations.RenameField(
            model_name='bill',
            old_name='bill_guitar_id',
            new_name='bill_guitar',
        ),
        migrations.RenameField(
            model_name='bill',
            old_name='bill_shop_id',
            new_name='bill_shop',
        ),
        migrations.AlterField(
            model_name='bill',
            name='purchase_datetime',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 15, 12, 6, 52, 155000)),
        ),
    ]
