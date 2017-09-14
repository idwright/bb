	
CREATE OR REPLACE VIEW duplicates AS	
SELECT dl.duplicate_id,
    oxcode.value as oxford_code,
    manage_sites_name,
    pf6_name,
    pv3name.value AS pv3_name,
    manage_sites_latitude,
    pf6_latitude,
    pv3latitude.value AS pv3_latitude,
    manage_sites_longitude,
    pf6_longitude,
    pv3longitude.value AS pv3_longitude
FROM
    dup_locs dl
    LEFT JOIN samples_with_location swlpv3 ON swlpv3.sample_id = dl.duplicate_id AND swlpv3.location_source =  'pv_3_locations'
    LEFT JOIN property_values pv3name ON pv3name.entity_id = swlpv3.location_id AND pv3name.prop_name='location'
    LEFT JOIN property_values pv3latitude ON pv3latitude.entity_id = swlpv3.location_id AND pv3latitude.prop_name='latitude'
    LEFT JOIN property_values pv3longitude ON pv3longitude.entity_id = swlpv3.location_id AND pv3longitude.prop_name='longitude'
    LEFT JOIN property_values oxcode ON oxcode.entity_id = dl.duplicate_id AND oxcode.prop_name='individual_code';
