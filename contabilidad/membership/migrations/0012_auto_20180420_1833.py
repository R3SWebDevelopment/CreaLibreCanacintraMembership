# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-20 23:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('membership', '0011_auto_20180418_2159'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3)),
                ('description', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3)),
                ('description', models.CharField(max_length=250)),
            ],
        ),
        migrations.AlterModelOptions(
            name='municipality',
            options={'ordering': ('state', 'name')},
        ),
        migrations.AlterModelOptions(
            name='state',
            options={'ordering': ('name',)},
        ),
        migrations.AddField(
            model_name='branch',
            name='sector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branches',
                                    to='membership.Sector'),
        ),
    ]