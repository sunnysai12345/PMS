# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-21 10:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_auto_20170320_1716'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='register',
            name='c_file',
        ),
        migrations.AddField(
            model_name='register',
            name='c_confirm_password',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='register',
            name='c_password',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
