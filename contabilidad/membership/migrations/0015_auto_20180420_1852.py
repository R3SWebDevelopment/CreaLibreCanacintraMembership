# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-20 23:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0014_auto_20180420_1846'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='branch',
            options={'ordering': ('sector', 'code', 'description')},
        ),
    ]