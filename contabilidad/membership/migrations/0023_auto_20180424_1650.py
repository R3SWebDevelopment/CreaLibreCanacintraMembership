# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-24 21:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0022_auto_20180424_1641'),
    ]

    operations = [
        migrations.RenameField(
            model_name='state',
            old_name='municipalities_list',
            new_name='municipalities',
        ),
    ]
