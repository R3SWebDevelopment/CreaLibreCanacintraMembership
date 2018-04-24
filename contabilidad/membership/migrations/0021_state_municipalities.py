# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-24 21:26
from __future__ import unicode_literals

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0020_state_zip_codes'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='municipalities',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.jsonb.JSONField(), default=None, null=True, size=None),
        ),
    ]
