# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-13 00:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0016_room_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room_type',
            name='description',
        ),
        migrations.AddField(
            model_name='room',
            name='description',
            field=models.CharField(default=1, max_length=400),
            preserve_default=False,
        ),
    ]
