# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2020-03-20 02:51
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('division', models.CharField(blank=True, max_length=64, null=True)),
                ('order', models.CharField(blank=True, max_length=64, null=True)),
                ('classname', models.CharField(blank=True, max_length=64, null=True)),
                ('sup_code', models.CharField(max_length=16)),
                ('legacy_pk', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Kingdom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.CharField(blank=True, max_length=256, null=True)),
                ('legacy_pk', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=512, null=True)),
                ('source_site', models.CharField(blank=True, max_length=128, null=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4283)),
                ('accuracy', models.IntegerField(blank=True, null=True)),
                ('legacy_pk', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=64, unique=True)),
                ('title', models.CharField(blank=True, max_length=128, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('custodian', models.CharField(blank=True, max_length=256, null=True)),
                ('custodian_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('source_type', models.CharField(blank=True, max_length=64, null=True)),
                ('url', models.URLField(blank=True, max_length=256, null=True)),
                ('download', models.CharField(max_length=10)),
                ('last_processed_on', models.DateField(blank=True, null=True)),
                ('last_updated_on', models.DateField(blank=True, null=True)),
                ('update_frequency', models.CharField(blank=True, max_length=256, null=True)),
                ('dataset_version', models.CharField(blank=True, max_length=64, null=True)),
                ('version_comments', models.TextField(blank=True, null=True)),
                ('display_in_directory_ind', models.CharField(blank=True, max_length=1, null=True)),
                ('vouchered_ind', models.CharField(blank=True, max_length=1, null=True)),
                ('core_dataset_ind', models.CharField(blank=True, max_length=1, null=True)),
                ('source_species_id_desc', models.CharField(blank=True, max_length=128, null=True)),
                ('full_search_ind', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('genus', models.CharField(max_length=128)),
                ('species', models.CharField(max_length=128)),
                ('infraspecies_rank', models.CharField(blank=True, max_length=64, null=True)),
                ('infraspecies_name', models.CharField(blank=True, max_length=128, null=True)),
                ('author', models.CharField(blank=True, max_length=512, null=True)),
                ('vernacular', models.CharField(blank=True, max_length=256, null=True)),
                ('currency_ind', models.CharField(max_length=1)),
                ('informal', models.CharField(blank=True, max_length=2, null=True)),
                ('naturalised_flag', models.CharField(blank=True, max_length=1, null=True)),
                ('consv_code', models.CharField(blank=True, max_length=4, null=True)),
                ('auth_name_ind', models.CharField(blank=True, max_length=1, null=True)),
                ('name_id', models.IntegerField(blank=True, null=True)),
                ('ranking', models.CharField(blank=True, max_length=8, null=True)),
                ('legacy_pk', models.IntegerField(unique=True)),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='naturemap2.Family')),
                ('kingdom', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='naturemap2.Kingdom')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='naturemap2.Source')),
            ],
        ),
        migrations.CreateModel(
            name='SpeciesLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.IntegerField(blank=True, null=True, unique=True)),
                ('query_date', models.DateField(blank=True, null=True)),
                ('collector', models.CharField(blank=True, max_length=128, null=True)),
                ('collector_no', models.CharField(blank=True, max_length=64, null=True)),
                ('survey', models.CharField(blank=True, max_length=128, null=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4283)),
                ('cust_group', models.CharField(blank=True, max_length=32, null=True)),
                ('stt_id', models.IntegerField(blank=True, null=True)),
                ('status_date', models.DateField(blank=True, null=True)),
                ('status_comments', models.CharField(blank=True, max_length=512, null=True)),
                ('hide_ind', models.CharField(blank=True, max_length=1, null=True)),
                ('legacy_pk', models.BigIntegerField(unique=True)),
                ('site', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='naturemap2.Site')),
                ('species', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='naturemap2.Species')),
            ],
        ),
        migrations.CreateModel(
            name='Supra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=32, unique=True)),
                ('name', models.CharField(blank=True, max_length=256, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='species',
            name='supra',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='naturemap2.Supra'),
        ),
        migrations.AddField(
            model_name='site',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='naturemap2.Source'),
        ),
        migrations.AddField(
            model_name='family',
            name='kingdom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='naturemap2.Kingdom'),
        ),
        migrations.AddField(
            model_name='family',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='naturemap2.Source'),
        ),
    ]
