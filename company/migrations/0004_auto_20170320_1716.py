# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-20 11:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_auto_20170319_2108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='register',
            name='c_ad_details',
        ),
        migrations.AddField(
            model_name='register',
            name='c_file',
            field=models.FileField(blank=True, upload_to='documents/'),
        ),
    ]
