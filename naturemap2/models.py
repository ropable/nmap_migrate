# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from django.template import Context, Template


class Source(models.Model):
    # `code` is the legacy PK.
    code = models.CharField(
        unique=True, max_length=64, help_text='The unique code for this source')
    title = models.CharField(
        max_length=128, blank=True, null=True,
        help_text='A brief title for the data source - appears in the web-page drop-down list')
    description = models.TextField(
        blank=True, null=True, help_text='A more fullsome description of the source')
    custodian = models.CharField(
        max_length=256, blank=True, null=True,
        help_text='The effective custodian of this data source')
    custodian_email = models.EmailField(blank=True, null=True)
    source_type = models.CharField(
        max_length=64, blank=True, null=True,
        help_text='Documents the source type eg species names, attribute values')
    url = models.URLField(
        max_length=256, blank=True, null=True,
        help_text='The URL for metadata describing this source. It may be used as an alternative to displaying local metadata.')
    download = models.CharField(max_length=10)
    last_processed_on = models.DateField(
        blank=True, null=True,
        help_text='The date the datasource ws last processed and updated in NatureMap')
    last_updated_on = models.DateField(
        blank=True, null=True,
        help_text='The date this datasource was last updated or modified by the custodian')
    update_frequency = models.CharField(max_length=256, blank=True, null=True)
    dataset_version = models.CharField(max_length=64, blank=True, null=True)
    version_comments = models.TextField(blank=True, null=True)
    # Cryptic fields:
    display_in_directory = models.NullBooleanField(default=None)
    vouchered = models.NullBooleanField(default=None)
    core_dataset = models.NullBooleanField(default=None)
    source_species_id_desc = models.CharField(max_length=128, blank=True, null=True)
    full_search = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Kingdom(models.Model):
    """
    This model is deprecated (data merged into Family).
    """
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True, null=True)
    legacy_pk = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


class Family(models.Model):
    """
    TODO: rename this model to something like Taxon.
    """
    # `name` is the legacy PK.
    name = models.CharField(max_length=64, help_text='Name of family')
    order = models.CharField(
        max_length=64, blank=True, null=True, help_text='The taxonomic order this family belongs to')
    class_name = models.CharField(
        max_length=64, blank=True, null=True, help_text='The taxonomic class this family belongs to')
    division = models.CharField(
        max_length=64, blank=True, null=True,
        help_text='The taxonomic division this family belongs to')  # Equivalent to phylum.
    kingdom_name = models.CharField(
        max_length=64, blank=True, null=True, help_text='The name of this kingdom')
    kingdom_description = models.CharField(
        max_length=256, blank=True, null=True, help_text='A description of this kingdom')
    sup_code = models.CharField(max_length=16, help_text='Supra-group code')
    source = models.ForeignKey(Source, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'families'

    def __str__(self):
        return self.name


class Supra(models.Model):
    """
    This model is deprecated (data merged into Species).
    """
    # `code` is the legacy PK.
    code = models.CharField(unique=True, max_length=32)
    name = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.name


class Species(models.Model):
    """95% sure that these are all the unique species names.
    """
    name = models.CharField(max_length=256, help_text='A concatenation of genus, species, rank and infra name')
    source = models.ForeignKey(Source, on_delete=models.PROTECT, help_text='The source of this name eg WACENSUS')
    family = models.ForeignKey(Family, on_delete=models.PROTECT, help_text='The family this species belongs to')
    supra_code = models.CharField(max_length=32, db_index=True, blank=True, null=True, help_text='Supra-group code')
    supra_name = models.CharField(max_length=256, blank=True, null=True, help_text='Description of supra-group')
    genus = models.CharField(max_length=128, help_text="The species' genus")
    species = models.CharField(max_length=128, help_text='The specific epithet for this taxon')
    infraspecies_rank = models.CharField(max_length=64, blank=True, null=True, help_text='The infraspecific rank of this taxon')
    infraspecies_name = models.CharField(max_length=128, blank=True, null=True, help_text='Infraspecific name')
    author = models.CharField(max_length=512, blank=True, null=True, help_text='The author of this taxon')
    vernacular = models.CharField(max_length=256, blank=True, null=True, help_text='The common name for this taxon')
    currency = models.BooleanField(default=True, help_text='A flag indicating whether this name is current.')
    informal = models.CharField(max_length=2, blank=True, null=True, help_text='Flag indicating whether this is a published name')
    naturalised = models.NullBooleanField(default=None, help_text='Flag indicating whether this taxon has been introduced into WA')
    consv_code = models.CharField(max_length=4, blank=True, null=True, help_text='The conservation code for this taxon, if known.')
    auth_name = models.NullBooleanField(default=None)  # Unclear what this field represents.
    name_id = models.IntegerField(blank=True, null=True, help_text='The original authoritative name_id of this name. If not null this number must be unique across all records.')
    ranking = models.CharField(max_length=8, blank=True, null=True)
    legacy_pk = models.IntegerField(unique=True)

    class Meta:
        verbose_name_plural = 'species'

    def __str__(self):
        return self.name


class Site(models.Model):
    """
    This model is deprecated (data merged into SpeciesLocation).
    """
    name = models.CharField(max_length=512, blank=True, null=True)
    source = models.ForeignKey(Source, on_delete=models.PROTECT)
    source_site = models.CharField(max_length=128, blank=True, null=True)
    point = models.PointField(srid=4283)
    accuracy = models.IntegerField(blank=True, null=True)
    legacy_pk = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


class SpeciesLocation(models.Model):
    """95% sure that this is "in the world" observations of each species.
    """
    identifier = models.IntegerField(unique=True, blank=True, null=True)
    species = models.ForeignKey(Species, on_delete=models.PROTECT)
    name = models.CharField(max_length=512, blank=True, null=True)
    query_date = models.DateField(blank=True, null=True)
    # Site fields
    site_name = models.CharField(max_length=512, blank=True, null=True, help_text='The name of the site, if it has one')
    site_source = models.ForeignKey(Source, blank=True, null=True, on_delete=models.PROTECT, help_text='The source of this site information')
    collector = models.CharField(max_length=128, blank=True, null=True)
    collector_no = models.CharField(max_length=64, blank=True, null=True)
    survey = models.CharField(max_length=128, blank=True, null=True)
    point = models.PointField(srid=4283)
    accuracy = models.IntegerField(blank=True, null=True, help_text='The spatial accuracy of the point (metres)')
    # Cryptic fields:
    cust_group = models.CharField(max_length=32, blank=True, null=True)
    stt_id = models.IntegerField(blank=True, null=True)
    status_date = models.DateField(blank=True, null=True)
    status_comments = models.CharField(max_length=512, blank=True, null=True)
    hide = models.NullBooleanField(default=None)
    legacy_pk = models.BigIntegerField(unique=True)
    document = models.TextField(blank=True, null=True)  # Used for full-text search indexing.
    metadata = JSONField(default=dict)

    def __str__(self):
        return self.name

    def get_document(self):
        # Render the document field value from a template.
        f = """{{ object.name }}
{{ species.family.name }}
{{ species.family.order }}
{{ species.family.class_name }}
{{ species.family.division }}
{{ species.family.kingdom_name }}
{% if species.vernacular %}{{ species.vernacular }}{% endif %}
{% if object.site_name %}{{ object.site_name }}{% endif %}
{% if object.collector %}{{ object.collector }}{% endif %}
"""
        template = Template(f)
        context = Context({'object': self, 'species': self.species})
        return template.render(context).strip()
