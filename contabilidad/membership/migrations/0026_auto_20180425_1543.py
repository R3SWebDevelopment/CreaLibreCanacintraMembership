# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-25 20:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0025_auto_20180425_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membershiprequest',
            name='branch',
            field=models.CharField(default=None, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='membershiprequest',
            name='sector',
            field=models.CharField(default=None, max_length=250, null=True),
        ),
    ]
