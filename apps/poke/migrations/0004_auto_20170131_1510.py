# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-31 23:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poke', '0003_auto_20170131_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='total_pokes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
