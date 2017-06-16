CREATE OR REPLACE VIEW `property_values` AS
	SELECT 
    HEX(e.id),
    e.added_id,
    ep.entity_id,
    p.id AS property_id,
    pt.id AS prop_type_id,
    pt.`source`,
    pt.`prop_name`,
    `pt`.`prop_type`,
    `pt`.`identity`,
    CASE pt.prop_type
        WHEN 'string' THEN CONVERT (p.string_value, CHAR CHARACTER SET utf8)
        WHEN 'integer' THEN CONVERT (p.long_value, CHAR CHARACTER SET utf8)
        WHEN 'boolean' THEN CASE p.boolean_value
								WHEN 0 THEN 'false'
                                WHEN 1 THEN 'true'
							END
        WHEN 'float' THEN CONVERT (p.float_value, CHAR CHARACTER SET utf8)
		WHEN 'double' THEN CONVERT (p.double_value, CHAR CHARACTER SET utf8)
        WHEN 'blob' THEN CONVERT (p.serializable_value, CHAR CHARACTER SET utf8)
        WHEN 'json' THEN CONVERT (p.json_value, CHAR CHARACTER SET utf8)
    END AS 'value'
	FROM
		`properties` AS p
			JOIN
				`property_types` AS pt ON pt.id = p.prop_type_id
			JOIN `entity_properties` AS ep ON ep.property_id = p.id
            JOIN `entities` AS e ON ep.entity_id = e.added_id;
                
CREATE OR REPLACE VIEW `associations` AS
	SELECT 
    HEX(s.id) as 'source_uuid',
    s.added_id as 'source_id',
    HEX(t.id) as 'target_uuid',
    t.added_id as 'target_id',
    a.assoc_name,
    ea.assoc_type_id
	FROM
		`entity_assoc` AS ea
			JOIN
				`entities` AS s ON ea.source_entity_id = s.added_id
			JOIN
				`entities` AS t ON ea.target_entity_id = t.added_id
			JOIN `assoc_types` AS a ON ea.assoc_type_id = a.id;

CREATE OR REPLACE VIEW `association_property_values` AS
    SELECT 
        HEX(s.id) AS 'source_uuid',
        s.added_id AS 'source_id',
        HEX(t.id) AS 'target_uuid',
        t.added_id AS 'target_id',
        a.assoc_name,
        ap.assoc_type_id,
        p.id AS property_id,
        pt.`source`,
        pt.`prop_name`,
        `pt`.`prop_type`,
        `pt`.`identity`,
        CASE pt.prop_type
            WHEN 'string' THEN CONVERT( p.string_value , CHAR CHARACTER SET UTF8)
            WHEN 'integer' THEN CONVERT( p.long_value , CHAR CHARACTER SET UTF8)
            WHEN 'boolean' THEN CONVERT( p.boolean_value , CHAR CHARACTER SET UTF8)
            WHEN 'float' THEN CONVERT( p.float_value , CHAR CHARACTER SET UTF8)
            WHEN 'double' THEN CONVERT( p.double_value , CHAR CHARACTER SET UTF8)
            WHEN 'blob' THEN CONVERT( p.serializable_value , CHAR CHARACTER SET UTF8)
            WHEN 'json' THEN CONVERT( p.json_value , CHAR CHARACTER SET UTF8)
        END AS 'value'
    FROM
        `assoc_properties` AS ap
            JOIN
        `entities` AS s ON ap.source_entity_id = s.added_id
            JOIN
        `entities` AS t ON ap.target_entity_id = t.added_id
            JOIN
        `assoc_types` AS a ON ap.assoc_type_id = a.id
            JOIN `properties` p ON ap.property_id = p.id
            JOIN `property_types` AS pt ON pt.id = p.prop_type_id;

CREATE OR REPLACE VIEW `implied_assocs` AS
    SELECT 
        spv.added_id AS source_id,
        tpv.added_id AS target_id,
        am.assoc_type_id,
        spv.value as key_value
    FROM
        assoc_mappings am
            JOIN
        properties sp ON sp.prop_type_id = am.source_prop_type_id
            JOIN
        properties tp ON tp.prop_type_id = am.target_prop_type_id
            JOIN
        property_values spv ON spv.property_id = sp.id
            JOIN
        property_values tpv ON tpv.property_id = tp.id
            JOIN
        assoc_types ast ON ast.id = am.assoc_type_id
    WHERE
        spv.value = tpv.value;
        
   CREATE OR REPLACE VIEW `implied_sources` AS
    SELECT 
        am.source_prop_type_id,
        am.target_prop_type_id,
        spt.`source`,
        spt.`prop_name`,
        tpv.prop_type,
        tpv.value AS key_value
    FROM
        assoc_mappings am
            LEFT JOIN
        properties sp ON sp.prop_type_id = am.source_prop_type_id
            JOIN
        property_types spt ON am.source_prop_type_id = spt.id
            JOIN
        properties tp ON tp.prop_type_id = am.target_prop_type_id
            LEFT JOIN
        property_values spv ON spv.property_id = sp.id
            JOIN
        property_values tpv ON tpv.property_id = tp.id
            JOIN
        assoc_types ast ON ast.id = am.assoc_type_id
    WHERE
        sp.id IS NULL OR tpv.value <> spv.value
    GROUP BY source_prop_type_id , target_prop_type_id , key_value , spv.`source` , prop_type;
     
