# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

"""
Read-only database models for access to legacy NMPSPECIES data.
"""

class Geographicdatums(models.Model):
    gda_value = models.IntegerField(primary_key=True)
    gda_constant = models.CharField(max_length=50)
    gda_short_description = models.CharField(max_length=50, blank=True, null=True)
    gda_description = models.CharField(max_length=100)
    gda_trans_value = models.IntegerField(blank=True, null=True)
    gda_trans_constant = models.CharField(max_length=200, blank=True, null=True)
    gda_trans_description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geographicdatums'

    def __str__(self):
        return self.gda_short_description


class Nmpsources(models.Model):
    sou_code = models.CharField(primary_key=True, max_length=30)
    sou_title = models.CharField(max_length=100, blank=True, null=True)
    sou_description = models.CharField(max_length=4000, blank=True, null=True)
    sou_custodian = models.CharField(max_length=240, blank=True, null=True)
    sou_custodian_email = models.CharField(max_length=100, blank=True, null=True)
    sou_source_type = models.CharField(max_length=30, blank=True, null=True)
    sou_url = models.CharField(max_length=250, blank=True, null=True)
    sou_download = models.CharField(max_length=10)
    sou_last_processed_on = models.DateField(blank=True, null=True)
    sou_last_updated_on = models.DateField(blank=True, null=True)
    sou_update_frequency = models.CharField(max_length=200, blank=True, null=True)
    sou_dataset_version = models.CharField(max_length=50, blank=True, null=True)
    sou_version_comments = models.CharField(max_length=4000, blank=True, null=True)
    sou_display_in_directory_ind = models.CharField(max_length=1, blank=True, null=True)
    sou_vouchered_ind = models.CharField(max_length=1, blank=True, null=True)
    sou_core_dataset_ind = models.CharField(max_length=1, blank=True, null=True)
    sou_source_species_id_desc = models.CharField(max_length=100, blank=True, null=True)
    sou_full_search_ind = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'nmpsources'

    def __str__(self):
        return self.sou_title


class Nmpsupra(models.Model):
    sup_code = models.CharField(primary_key=True, max_length=10)
    sup_name = models.CharField(max_length=240, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nmpsupra'

    def __str__(self):
        return self.sup_name


class Nmpkingdoms(models.Model):
    kin_id = models.IntegerField(primary_key=True)
    kin_name = models.CharField(max_length=15)
    kin_description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nmpkingdoms'

    def __str__(self):
        return self.kin_name


class Nmpfamilies(models.Model):
    fam_name = models.CharField(primary_key=True, max_length=40)
    fam_kin = models.ForeignKey('Nmpkingdoms', models.DO_NOTHING)
    fam_division = models.CharField(max_length=40, blank=True, null=True)
    fam_order = models.CharField(max_length=40, blank=True, null=True)
    fam_class = models.CharField(max_length=40, blank=True, null=True)
    fam_sup_code = models.CharField(max_length=10)
    fam_sou_code = models.ForeignKey('Nmpsources', models.DO_NOTHING, db_column='fam_sou_code')

    class Meta:
        managed = False
        db_table = 'nmpfamilies'

    def __str__(self):
        return self.fam_name


class Nmpsites(models.Model):
    """These are all the unique sites where species have been collected.
    """
    sit_id = models.IntegerField(primary_key=True)
    sit_name = models.CharField(max_length=400, blank=True, null=True)
    sit_sou_code = models.ForeignKey('Nmpsources', models.DO_NOTHING, db_column='sit_sou_code')
    sit_source_site = models.CharField(max_length=100, blank=True, null=True)
    sit_longitude = models.DecimalField(max_digits=13, decimal_places=8)
    sit_latitude = models.DecimalField(max_digits=13, decimal_places=8)
    sit_accuracy = models.IntegerField(blank=True, null=True)
    sit_gda_value = models.ForeignKey('Geographicdatums', models.DO_NOTHING, db_column='sit_gda_value')

    class Meta:
        managed = False
        db_table = 'nmpsites'

    def __str__(self):
        return self.sit_name


class Nmpspeciesnames(models.Model):
    """These are all the unique species/taxa names.
    """
    spn_id = models.IntegerField(primary_key=True)
    spn_name = models.CharField(max_length=240)
    spn_sou_code = models.ForeignKey('Nmpsources', models.DO_NOTHING, db_column='spn_sou_code')
    spn_currency_ind = models.CharField(max_length=1)
    spn_kin = models.ForeignKey('Nmpkingdoms', models.DO_NOTHING)
    spn_fam_name = models.ForeignKey('Nmpfamilies', models.DO_NOTHING, db_column='spn_fam_name')
    spn_genus = models.CharField(max_length=40)
    spn_species = models.CharField(max_length=70)
    spn_infrasp_rank = models.CharField(max_length=9, blank=True, null=True)
    spn_infrasp_name = models.CharField(max_length=70, blank=True, null=True)
    spn_author = models.CharField(max_length=300, blank=True, null=True)
    spn_informal = models.CharField(max_length=2, blank=True, null=True)
    spn_naturalised_flag = models.CharField(max_length=1, blank=True, null=True)
    spn_vernacular = models.CharField(max_length=200, blank=True, null=True)
    spn_sup_code = models.ForeignKey('Nmpsupra', models.DO_NOTHING, db_column='spn_sup_code')
    spn_consv_code = models.CharField(max_length=3, blank=True, null=True)
    spn_auth_name_ind = models.CharField(max_length=1, blank=True, null=True)
    spn_name_id = models.IntegerField(blank=True, null=True)
    spn_ranking = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nmpspeciesnames'

    def __str__(self):
        return self.spn_name


class Nmpspecies(models.Model):
    """This is the table which links species to the sites at which they have been collected.
    """
    objectid = models.BigIntegerField(primary_key=True)
    spe_id = models.IntegerField(unique=True, blank=True, null=True)
    spe_spn = models.ForeignKey('Nmpspeciesnames', models.DO_NOTHING, blank=True, null=True)
    spe_name = models.CharField(max_length=120, blank=True, null=True)
    spe_sou_code = models.ForeignKey('Nmpsources', models.DO_NOTHING, db_column='spe_sou_code', blank=True, null=True)
    spe_source_species_id = models.CharField(max_length=110, blank=True, null=True)
    spe_coldate_dy = models.CharField(max_length=2, blank=True, null=True)
    spe_coldate_mn = models.CharField(max_length=2, blank=True, null=True)
    spe_coldate_yr = models.CharField(max_length=4, blank=True, null=True)
    spe_sit = models.ForeignKey('Nmpsites', models.DO_NOTHING, blank=True, null=True)
    spe_collector = models.CharField(max_length=100, blank=True, null=True)
    spe_collector_no = models.CharField(max_length=30, blank=True, null=True)
    spe_survey = models.CharField(max_length=100, blank=True, null=True)
    spe_sup_code = models.ForeignKey('Nmpsupra', models.DO_NOTHING, db_column='spe_sup_code', blank=True, null=True)
    spe_kin = models.ForeignKey('Nmpkingdoms', models.DO_NOTHING, blank=True, null=True)
    spe_longitude = models.DecimalField(max_digits=38, decimal_places=8, blank=True, null=True)
    spe_latitude = models.DecimalField(max_digits=38, decimal_places=8, blank=True, null=True)
    spe_gda_value = models.IntegerField(blank=True, null=True)
    spe_gda_latitude = models.DecimalField(max_digits=38, decimal_places=8, blank=True, null=True)
    spe_gda_longitude = models.DecimalField(max_digits=38, decimal_places=8, blank=True, null=True)
    spe_cust_group = models.CharField(max_length=20, blank=True, null=True)
    spe_query_date = models.DateField(blank=True, null=True)
    spe_stt_id = models.IntegerField(blank=True, null=True)
    spe_status_date = models.DateField(blank=True, null=True)
    spe_status_comments = models.CharField(max_length=300, blank=True, null=True)
    shape = models.TextField(blank=True, null=True)
    spe_hide_ind = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nmpspecies'

    def __str__(self):
        return self.spe_name
