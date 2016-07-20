# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-12 15:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.FloatField()),
                ('executed_time', models.TimeField()),
                ('in_zone', models.TimeField()),
                ('average_heart_rate', models.IntegerField()),
            ],
        ),
    ]
