# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-01-20 02:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naturemap2', '0015_auto_20200429_0758'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specieslocation',
            name='name',
        ),
        migrations.AddField(
            model_name='specieslocation',
            name='collected_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
