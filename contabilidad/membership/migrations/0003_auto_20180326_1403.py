# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-26 20:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0002_member_rfc'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='business_contact',
            field=models.CharField(default=None, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='membership_feed',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=12, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='payment_date',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='promoter_name',
            field=models.CharField(default=None, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='promoter_office',
            field=models.CharField(default=None, max_length=250, null=True),
        ),
    ]
