# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-24 14:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0017_tarifffraction'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suburb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('zip_code', models.CharField(max_length=5)),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suburbs', to='membership.Municipality')),
            ],
            options={
                'ordering': ('municipality', 'name'),
            },
        ),
    ]