# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.gis.db import models


class Source(models.Model):
    # `code` is the legacy PK.
    code = models.CharField(unique=True, max_length=64)
    title = models.CharField(max_length=128, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    custodian = models.CharField(max_length=256, blank=True, null=True)
    custodian_email = models.EmailField(blank=True, null=True)
    source_type = models.CharField(max_length=64, blank=True, null=True)
    url = models.URLField(max_length=256, blank=True, null=True)
    download = models.CharField(max_length=10)
    last_processed_on = models.DateField(blank=True, null=True)
    last_updated_on = models.DateField(blank=True, null=True)
    update_frequency = models.CharField(max_length=256, blank=True, null=True)
    dataset_version = models.CharField(max_length=64, blank=True, null=True)
    version_comments = models.TextField(blank=True, null=True)
    # Cryptic fields:
    display_in_directory = models.NullBooleanField(default=None)
    vouchered = models.NullBooleanField(default=None)
    core_dataset_ind = models.CharField(max_length=1, blank=True, null=True)
    source_species_id_desc = models.CharField(max_length=128, blank=True, null=True)
    full_search = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Site(models.Model):
    name = models.CharField(max_length=512, blank=True, null=True)
    source = models.ForeignKey(Source, on_delete=models.DO_NOTHING)
    source_site = models.CharField(max_length=128, blank=True, null=True)
    point = models.PointField(srid=4283)
    accuracy = models.IntegerField(blank=True, null=True)
    legacy_pk = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


class Kingdom(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True, null=True)
    legacy_pk = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


class Family(models.Model):
    # `name` is the legacy PK.
    name = models.CharField(max_length=64)
    kingdom = models.ForeignKey(Kingdom, on_delete=models.PROTECT)
    division = models.CharField(max_length=64, blank=True, null=True)
    order = models.CharField(max_length=64, blank=True, null=True)
    classname = models.CharField(max_length=64, blank=True, null=True)
    sup_code = models.CharField(max_length=16)
    source = models.ForeignKey(Source, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'families'

    def __str__(self):
        return self.name


class Supra(models.Model):
    """Seems to be a general 'common use' division.
    """
    # `code` is the legacy PK.
    code = models.CharField(unique=True, max_length=32)
    name = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.name


class Species(models.Model):
    """95% sure that these are all the unique species names.
    """
    name = models.CharField(max_length=256)
    source = models.ForeignKey(Source, on_delete=models.PROTECT)
    kingdom = models.ForeignKey(Kingdom, on_delete=models.PROTECT)
    family = models.ForeignKey(Family, on_delete=models.PROTECT)
    supra = models.ForeignKey(Supra, on_delete=models.PROTECT)
    genus = models.CharField(max_length=128)
    species = models.CharField(max_length=128)
    infraspecies_rank = models.CharField(max_length=64, blank=True, null=True)
    infraspecies_name = models.CharField(max_length=128, blank=True, null=True)
    author = models.CharField(max_length=512, blank=True, null=True)
    vernacular = models.CharField(max_length=256, blank=True, null=True)
    # Cryptic fields:
    currency = models.BooleanField(default=True)  # 95% sure this is 'current name'.
    informal = models.CharField(max_length=2, blank=True, null=True)
    naturalised = models.NullBooleanField(default=None)
    consv_code = models.CharField(max_length=4, blank=True, null=True)
    auth_name = models.NullBooleanField(default=None)
    name_id = models.IntegerField(blank=True, null=True)
    ranking = models.CharField(max_length=8, blank=True, null=True)
    legacy_pk = models.IntegerField(unique=True)

    class Meta:
        verbose_name_plural = 'species'

    def __str__(self):
        return self.name


class SpeciesLocation(models.Model):
    """95% sure that this is "in the world" observations of each species.
    """
    identifier = models.IntegerField(unique=True, blank=True, null=True)
    species = models.ForeignKey(Species, on_delete=models.PROTECT)
    query_date = models.DateField(blank=True, null=True)
    site = models.ForeignKey(Site, on_delete=models.PROTECT, blank=True, null=True)
    collector = models.CharField(max_length=128, blank=True, null=True)
    collector_no = models.CharField(max_length=64, blank=True, null=True)
    survey = models.CharField(max_length=128, blank=True, null=True)
    point = models.PointField(srid=4283)
    # Cryptic fields:
    cust_group = models.CharField(max_length=32, blank=True, null=True)
    stt_id = models.IntegerField(blank=True, null=True)
    status_date = models.DateField(blank=True, null=True)
    status_comments = models.CharField(max_length=512, blank=True, null=True)
    hide = models.NullBooleanField(default=None)
    legacy_pk = models.BigIntegerField(unique=True)

    def __str__(self):
        return self.species.name
