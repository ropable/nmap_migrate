# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-03-30 02:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('naturemap2', '0013_auto_20200327_0844'),
    ]

    operations = [
        migrations.RenameField(
            model_name='specieslocation',
            old_name='data',
            new_name='metadata',
        ),
    ]