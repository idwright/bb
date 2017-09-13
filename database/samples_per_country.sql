-- The following 2 are equivalent
-- SELECT * FROM entities_by_type pv WHERE string_value='location'
-- SELECT * FROM property_values pv WHERE pv.prop_name='entity_type' AND pv.value='location'
-- but for some reason the later is much faster when used in samples_with_location
CREATE OR replace VIEW entities_by_type AS 
	SELECT ep.entity_id,p.string_value FROM property_types pt 
		JOIN properties p ON p.prop_type_id = pt.id 
		JOIN entity_properties ep ON ep.property_id = p.id
		WHERE source='system' and prop_name='entity_type';


CREATE OR REPLACE VIEW duplicate_locations AS
	SELECT pv.added_id AS duplicate_id, pv.source as prop_source, pv.value as oxford_code
    FROM property_values pv
    WHERE pv.prop_name='oxford_code' AND pv.entity_id IN 
		(SELECT entity_id FROM property_values 	WHERE prop_name='location'
			GROUP BY entity_id,prop_name HAVING COUNT(*) > 1);

    
CREATE OR REPLACE VIEW samples_with_location AS
	SELECT ea.target_entity_id as sample_id, ea.source_entity_id as location_id, 
            ls.source AS location_source
    FROM entity_assoc ea
		JOIN assoc_types asst ON ea.assoc_type_id = asst.id
		JOIN (SELECT * FROM property_values pv WHERE pv.prop_name='entity_type' AND pv.value='location') AS pv ON pv.entity_id = ea.source_entity_id  
		JOIN (SELECT * FROM property_values pv WHERE pv.prop_name='entity_type' AND pv.value='sample') pvl ON pvl.entity_id = ea.target_entity_id
        JOIN (SELECT added_id,source FROM property_values WHERE identity = true) ls ON ls.added_id = ea.source_entity_id;

--        LEFT JOIN duplicate_locations dl ON dl.duplicate_id = ea.target_entity_id AND dl.prop_source = 'pf_6_metadata'
--       LEFT JOIN duplicate_locations dl3 ON dl.duplicate_id = ea.target_entity_id AND dl.prop_source = 'pv_3_sanger_source_code_metadata'
--      WHERE dl.prop_source IS NULL OR 
--            (dl.prop_source IS NOT NULL AND ls.source = 'manage_sites') OR
--           (dl3.prop_source IS NOT NULL AND ls.source = 'manage_sites');
        
CREATE OR REPLACE VIEW samples_per_country AS
	SELECT pcnt.value AS country, COUNT(pcnt.value) AS samples FROM samples_with_location sl
		JOIN property_values pcnt ON pcnt.entity_id = sl.location_id AND pcnt.prop_name='country'
		GROUP BY pcnt.value;
        

-- This is very slow use as part of CREATE TABLE dup_locs AS SELECT * FROM duplicate_locations;
-- Actually too slow to use - over 2 days
-- without pv3 ~45 minutes
CREATE OR REPLACE VIEW duplicate_location_values AS
	SELECT pv.duplicate_id, pv.oxford_code,
		msname.value AS manage_sites_name, pf6name.value AS pf6_name, pv3name.value AS pv3_name,
		mslatitude.value AS manage_sites_latitude, pf6latitude.value AS pf6_latitude, pv3latitude.value AS pv3_latitude,
		mslongitude.value AS manage_sites_longitude, pf6longitude.value AS pf6_longitude, pv3longitude.value AS pv3_longitude
        FROM duplicate_locations pv
		LEFT JOIN samples_with_location swl ON swl.sample_id = pv.duplicate_id AND swl.location_source =  'manage_sites'
        LEFT JOIN samples_with_location swlpf6 ON swlpf6.sample_id = pv.duplicate_id AND swlpf6.location_source =  'location_pf_6'
        LEFT JOIN samples_with_location swlpv3 ON swlpv3.sample_id = pv.duplicate_id AND swlpv3.location_source =  'pv_3_sanger_source_code_metadata'
        LEFT JOIN property_values msname ON msname.entity_id = swl.location_id AND msname.prop_name='name'
        LEFT JOIN property_values pf6name ON pf6name.entity_id = swlpf6.location_id AND pf6name.prop_name='location'
        LEFT JOIN property_values pv3name ON pf6name.entity_id = swlpv3.location_id AND pv3name.prop_name='location'
        LEFT JOIN property_values mslatitude ON mslatitude.entity_id = swl.location_id AND mslatitude.prop_name='latitude'
        LEFT JOIN property_values pf6latitude ON pf6latitude.entity_id = swlpf6.location_id AND pf6latitude.prop_name='latitude'
        LEFT JOIN property_values pv3latitude ON pv3latitude.entity_id = swlpv3.location_id AND pv3latitude.prop_name='latitude'
        LEFT JOIN property_values mslongitude ON mslongitude.entity_id = swl.location_id AND mslongitude.prop_name='longitude'
        LEFT JOIN property_values pf6longitude ON pf6longitude.entity_id = swlpf6.location_id AND pf6longitude.prop_name='longitude'
        LEFT JOIN property_values pv3longitude ON pv3longitude.entity_id = swlpv3.location_id AND pv3longitude.prop_name='longitude';
		
