# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-26 20:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('membership', '0003_auto_20180326_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='allowed_person',
            field=models.ManyToManyField(related_name='members', to=settings.AUTH_USER_MODEL),
        ),
    ]
