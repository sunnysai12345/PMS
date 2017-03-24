# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-24 13:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_auto_20170321_1533'),
    ]

    operations = [
        migrations.CreateModel(
            name='Edit_Details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_name', models.CharField(blank=True, max_length=20, null=True)),
                ('c_email', models.EmailField(blank=True, max_length=254)),
                ('c_ctc_offered', models.DecimalField(blank=True, decimal_places=2, max_digits=8)),
                ('c_branches_allowed', models.TextField(blank=True)),
                ('c_requirements', models.TextField(blank=True)),
                ('c_selected_students', models.FileField(blank=True, upload_to='documents/')),
                ('c_perm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.Register')),
            ],
        ),
    ]
