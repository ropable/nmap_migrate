# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Source, Site, Kingdom, Family, Supra, Species, SpeciesLocation


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('code', 'title','custodian', 'source_type')
    readonly_fields = ('code',)
    search_fields = ('code', 'title', 'custodian')


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'source', 'source_site')
    readonly_fields = ('legacy_pk',)
    search_fields = ('name',)


@admin.register(Kingdom)
class KingdomAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    readonly_fields = ('legacy_pk',)


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'class_name', 'division', 'kingdom_name', 'sup_code')
    readonly_fields = ('name',)
    search_fields = ('name', 'order', 'class_name', 'division', 'kingdom_name', 'sup_code')


@admin.register(Supra)
class SupraAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    readonly_fields = ('code',)
    search_fields = ('code', 'name')


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('name', 'family', 'supra_code', 'vernacular', 'currency', 'consv_code')
    list_filter = ('supra_code', 'currency', 'consv_code')
    raw_id_fields = ('family',)
    readonly_fields = ('legacy_pk',)
    search_fields = ('name', 'author', 'vernacular')


@admin.register(SpeciesLocation)
class SpeciesLocationAdmin(admin.ModelAdmin):
    date_hierarchy = 'query_date'
    list_display = ('name', 'site_name', 'collector', 'query_date', 'hide')
    list_filter = ('hide',)
    raw_id_fields = ('species',)
    readonly_fields = ('legacy_pk',)
    search_fields = ('name', 'site_name', 'collector', 'survey')
