from django.contrib.gis.geos import Point
from nmpspecies.models import (
    Nmpsources, Nmpsites, Nmpkingdoms, Nmpfamilies, Nmpsupra, Nmpspeciesnames, Nmpspecies
)
from .models import (
    Source, Site, Kingdom, Family, Supra, Species, SpeciesLocation
)


def import_nmap_data():
    """Import script to methodically import all of the NMAP schema data.
    Import should be idempotent.
    """
    # Bulk create Sources.
    create_list = []
    for source in Nmpsources.objects.all():
        if not Source.objects.filter(code=source.sou_code).exists():
            create_list.append(Source(
                code=source.sou_code,
                title=source.sou_title,
                description=source.sou_description,
                custodian=source.sou_custodian,
                custodian_email=source.sou_custodian_email,
                source_type=source.sou_source_type,
                url=source.sou_url,
                download=source.sou_download,
                last_processed_on=source.sou_last_processed_on,
                last_updated_on=source.sou_last_updated_on,
                update_frequency=source.sou_update_frequency,
                dataset_version=source.sou_dataset_version,
                version_comments=source.sou_version_comments,
                display_in_directory=source.sou_display_in_directory_ind == 'Y',
                vouchered=source.sou_vouchered_ind == 'Y',
                core_dataset=source.sou_core_dataset_ind == 'Y',
                source_species_id_desc=source.sou_source_species_id_desc,
                full_search=source.sou_full_search_ind == 'Y',
            ))
    print('Creating {} Source objects'.format(len(create_list)))
    Source.objects.bulk_create(create_list)

    # Bulk create Kingdoms
    create_list = []
    for kingdom in Nmpkingdoms.objects.all():
        if not Kingdom.objects.filter(legacy_pk=kingdom.kin_id).exists():
            create_list.append(Kingdom(
                name=kingdom.kin_name,
                description=kingdom.kin_description,
                legacy_pk=kingdom.kin_id,
            ))
    print('Creating {} Kingdom objects'.format(len(create_list)))
    Kingdom.objects.bulk_create(create_list)

    # Bulk create Families in batches of 1000.
    total = Nmpfamilies.objects.count()
    for i in range(0, total, 1000):
        print('Querying features {} to {} of {}'.format(i, i + 1000, total))
        create_list = []
        for fam in Nmpfamilies.objects.order_by('fam_name')[i:i + 1000]:
            if not Family.objects.filter(name=fam.fam_name).exists():
                kingdom = Kingdom.objects.get(legacy_pk=fam.fam_kin_id)
                create_list.append(Family(
                    name=fam.fam_name,
                    kingdom_name=kingdom.name,
                    kingdom_description=kingdom.description,
                    division=fam.fam_division,
                    order=fam.fam_order,
                    class_name=fam.fam_class,
                    sup_code=fam.fam_sup_code,
                    source=Source.objects.get(code=fam.fam_sou_code_id),
                ))
        print('Creating {} Family objects'.format(len(create_list)))
        Family.objects.bulk_create(create_list)

    # Bulk create Supras
    create_list = []
    for supra in Nmpsupra.objects.all():
        if not Supra.objects.filter(code=supra.sup_code).exists():
            create_list.append(Supra(
                code=supra.sup_code,
                name=supra.sup_name,
            ))
    print('Creating {} Supra objects'.format(len(create_list)))
    Supra.objects.bulk_create(create_list)

    # Bulk create Species in batches of 1000.
    total = Nmpspeciesnames.objects.count()
    for i in range(0, total, 1000):
        print('Querying features {} to {} of {}'.format(i, i + 1000, total))
        create_list = []
        for sp in Nmpspeciesnames.objects.order_by('spn_id')[i:i + 1000]:
            if not Species.objects.filter(legacy_pk=sp.spn_id).exists():
                supra = Supra.objects.get(code=sp.spn_sup_code_id)
                create_list.append(Species(
                    name=sp.spn_name,
                    source=Source.objects.get(code=sp.spn_sou_code_id),
                    family=Family.objects.get(name=sp.spn_fam_name_id),
                    supra_code=supra.code,
                    supra_name=supra.name,
                    genus=sp.spn_genus,
                    species=sp.spn_species,
                    infraspecies_rank=sp.spn_infrasp_rank,
                    infraspecies_name=sp.spn_infrasp_name,
                    author=sp.spn_author,
                    informal=sp.spn_informal,
                    naturalised=sp.spn_naturalised_flag == 'Y',
                    vernacular=sp.spn_vernacular,
                    currency=sp.spn_currency_ind == 'Y',
                    consv_code=sp.spn_consv_code,
                    auth_name=sp.spn_auth_name_ind == 'Y',
                    name_id=sp.spn_name_id,
                    ranking=sp.spn_ranking,
                    legacy_pk=sp.spn_id,
                ))
        print('Creating {} Species objects'.format(len(create_list)))
        Species.objects.bulk_create(create_list)

    # Bulk create Sites in batches of 1000.
    total = Nmpsites.objects.count()
    for i in range(0, total, 1000):
        print('Querying features {} to {} of {}'.format(i, i + 1000, total))
        create_list = []
        for site in Nmpsites.objects.order_by('sit_id')[i:i + 1000]:
            if not Site.objects.filter(legacy_pk=site.sit_id).exists():
                create_list.append(Site(
                    name=site.sit_name,
                    source=Source.objects.get(code=site.sit_sou_code_id),
                    source_site=site.sit_source_site,
                    point=Point((site.sit_longitude, site.sit_latitude), srid=4283),
                    accuracy=site.sit_accuracy,
                    legacy_pk=site.sit_id,
                ))
        print('Creating {} Site objects'.format(len(create_list)))
        Site.objects.bulk_create(create_list)

    # Bulk create SpeciesLocation in batches of 1000.
    total = Nmpspecies.objects.count()
    for i in range(0, total, 1000):
        print('Querying features {} to {} of {}'.format(i, i + 1000, total))
        create_list = []
        for sp in Nmpspecies.objects.order_by('objectid')[i:i + 1000]:
            if not SpeciesLocation.objects.filter(legacy_pk=sp.objectid).exists():
                site = Site.objects.get(legacy_pk=sp.spe_sit_id)
                spl = SpeciesLocation(
                    identifier=sp.spe_id,
                    species=Species.objects.get(legacy_pk=sp.spe_spn_id),
                    query_date=sp.spe_query_date,
                    site_name=site.name,
                    site_source=site.source,
                    collector=sp.spe_collector,
                    collector_no=sp.spe_collector_no,
                    survey=sp.spe_survey,
                    point=Point((sp.spe_longitude, sp.spe_latitude), srid=4283),
                    cust_group=sp.spe_cust_group,
                    stt_id=sp.spe_stt_id,
                    status_date=sp.spe_status_date,
                    status_comments=sp.spe_status_comments,
                    hide=sp.spe_hide_ind == 'Y',
                    legacy_pk=sp.objectid,
                )
                spl.document = spl.get_document()
                d = {
                    'species': spl.species.species,
                    'genus': spl.species.genus,
                    'family': spl.species.family.name
                }
                if spl.species.family.order:
                    d['order'] = spl.species.family.order
                if spl.species.family.class_name:
                    d['class'] = spl.species.family.class_name
                if spl.species.family.division:
                    d['division'] = spl.species.family.division
                if spl.species.family.kingdom_name:
                    d['kingdom'] = spl.species.family.kingdom_name
                if spl.species.consv_code:
                    d['consv_code'] = spl.species.consv_code
                spl.metadata = d
                create_list.append(spl)
        print('Creating {} SpeciesLocation objects'.format(len(create_list)))
        SpeciesLocation.objects.bulk_create(create_list)
