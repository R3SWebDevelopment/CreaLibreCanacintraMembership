# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-24 21:41
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0021_state_municipalities'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='state',
            name='municipalities',
        ),
        migrations.AddField(
            model_name='state',
            name='municipalities_list',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list, null=True),
        ),
    ]