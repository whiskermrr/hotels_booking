# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-08 12:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0010_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='media/images'),
        ),
    ]