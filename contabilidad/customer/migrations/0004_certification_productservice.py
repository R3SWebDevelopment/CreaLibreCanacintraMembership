# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-03 04:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_auto_20180418_1056'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=250)),
            ],
            options={
                'ordering': ('code', 'name'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=250)),
            ],
            options={
                'ordering': ('code', 'name'),
                'abstract': False,
            },
        ),
    ]