# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-18 19:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0009_auto_20180418_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='updaterequest',
            name='rfc',
            field=models.CharField(default=None, max_length=13, null=True),
        ),
    ]