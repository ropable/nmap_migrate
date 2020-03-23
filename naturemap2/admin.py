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
    list_display = ('name', 'kingdom', 'division', 'order', 'classname')
    readonly_fields = ('name',)
    search_fields = ('name', 'kingdom__name', 'division', 'order', 'classname')


@admin.register(Supra)
class SupraAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    readonly_fields = ('code',)
    search_fields = ('code', 'name')


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('name', 'kingdom', 'family', 'supra', 'author')
    list_filter = ('kingdom', 'supra')
    readonly_fields = ('legacy_pk',)
    search_fields = ('name', 'author', 'vernacular')


@admin.register(SpeciesLocation)
class SpeciesLocationAdmin(admin.ModelAdmin):
    date_hierarchy = 'query_date'
    list_display = ('species', 'site', 'collector', 'query_date')
    readonly_fields = ('legacy_pk',)
    search_fields = ('species__name', 'site__name', 'collector', 'survey')
