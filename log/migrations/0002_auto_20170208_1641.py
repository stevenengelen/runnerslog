# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-08 16:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='planned_duration',
            field=models.DurationField(help_text='HH:MM', null=True, verbose_name='Planned duration: '),
        ),
        migrations.AlterField(
            model_name='training',
            name='average_heart_rate',
            field=models.IntegerField(verbose_name='Average heart rate: '),
        ),
        migrations.AlterField(
            model_name='training',
            name='distance',
            field=models.FloatField(verbose_name='Distance: '),
        ),
        migrations.AlterField(
            model_name='training',
            name='executed_time',
            field=models.DurationField(help_text='HH:MM:SS', verbose_name='Executed time: '),
        ),
        migrations.AlterField(
            model_name='training',
            name='in_zone',
            field=models.DurationField(help_text='HH:MM:SS', verbose_name='In zone: '),
        ),
    ]
