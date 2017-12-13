# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-13 00:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0017_auto_20171213_0146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='smoking_in',
        ),
        migrations.AddField(
            model_name='room_type',
            name='smoking_in',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]