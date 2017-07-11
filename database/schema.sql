DROP TABLE IF EXISTS `assoc_properties`;
DROP TABLE IF EXISTS `entity_assoc`;
DROP TABLE IF EXISTS `assoc_mappings`;
DROP TABLE IF EXISTS `assoc_types`;
DROP TABLE IF EXISTS `entity_properties`;
DROP TABLE IF EXISTS `properties`;
DROP TABLE IF EXISTS `property_types`;
DROP TABLE IF EXISTS `entities`;

CREATE TABLE `entities` (
	`added_id` bigint(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `id` binary(16) NOT NULL,
    UNIQUE KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `property_types` (
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `source` varchar(32) NOT NULL,
    `prop_name` varchar(64) NOT NULL,
    `prop_type` varchar(32) DEFAULT 'string',
    `prop_order` int(4) DEFAULT 0,
    `identity` bit(1) DEFAULT NULL,
    `versionable` bit(1) DEFAULT 1,
    PRIMARY KEY (`id`),
    UNIQUE KEY `psn` (`source`, `prop_name`),
    UNIQUE KEY `psnt` (`source`, `prop_name`, `prop_type`),
    KEY `identity` (`identity`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE `properties` (
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `prop_type_id` bigint(20) NOT NULL,
    `boolean_value` bit(1) DEFAULT NULL,
    `long_value` bigint(20) DEFAULT NULL,
    `float_value` decimal(6,3) DEFAULT NULL,
    `double_value` decimal(12,6) DEFAULT NULL,
    `string_value` text DEFAULT NULL,
    `serializable_value` blob DEFAULT NULL,
    `json_value` JSON DEFAULT NULL,
    `datetime_value` datetime DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `eprop_id` (`prop_type_id`),
    KEY `string_value` (`string_value`(255)),
    KEY `svt` (`prop_type_id`, `string_value`(255)),
    KEY `long_value` (`long_value`),
    CONSTRAINT `fk_prop_type_id` FOREIGN KEY (`prop_type_id`) REFERENCES `property_types` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE `entity_properties` (
    `entity_id` bigint(20) NOT NULL,
    `property_id` bigint(20) NOT NULL,
    PRIMARY KEY (`entity_id`, `property_id`),
    KEY `fk_ep_pid` (`property_id`),
    KEY `fk_ep_eid` (`entity_id`),
    CONSTRAINT `fk_ent_prop_ent` FOREIGN KEY (`entity_id`) REFERENCES `entities` (`added_id`),
    CONSTRAINT `fk_ent_prop_prop` FOREIGN KEY (`property_id`) REFERENCES `properties` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `assoc_types` (
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `assoc_name` varchar(128) NOT NULL,
    `assoc_type` varchar(32) NOT NULL DEFAULT 'parent-child',
    PRIMARY KEY (`id`),
    UNIQUE KEY `an` (`assoc_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `entity_assoc` (
      `source_entity_id` bigint(20) NOT NULL,
      `target_entity_id` bigint(20) NOT NULL,
      `assoc_type_id` bigint(20) NOT NULL,
      PRIMARY KEY `ea_pk` (`source_entity_id`,`target_entity_id`,`assoc_type_id`),
      KEY `fk_ent_nass_snode` (`source_entity_id`,`assoc_type_id`),
      KEY `fk_ent_nass_tnode` (`target_entity_id`,`assoc_type_id`),
      KEY `fk_ent_nass_tt` (`assoc_type_id`),
      CONSTRAINT `fk_ent_nass_snode` FOREIGN KEY (`source_entity_id`) REFERENCES `entities` (`added_id`),
      CONSTRAINT `fk_ent_nass_tnode` FOREIGN KEY (`target_entity_id`) REFERENCES `entities` (`added_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `assoc_properties` (
    `source_entity_id` bigint(20) NOT NULL,
    `target_entity_id` bigint(20) NOT NULL,
    `assoc_type_id` bigint(20) NOT NULL,
    `property_id` bigint(20) NOT NULL,
    PRIMARY KEY `ap_pk` (`source_entity_id`,`target_entity_id`,`assoc_type_id`, `property_id`),
    KEY `fk_ap_pid` (`property_id`),
    CONSTRAINT `fk_assoc_prop_ent` FOREIGN KEY (`source_entity_id`,`target_entity_id`,`assoc_type_id`) REFERENCES `entity_assoc` (`source_entity_id`,`target_entity_id`,`assoc_type_id`),
    CONSTRAINT `fk_assoc_prop_prop` FOREIGN KEY (`property_id`) REFERENCES `properties` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `assoc_mappings` (
	`source_prop_type_id` bigint(20) NOT NULL,
    `target_prop_type_id` bigint(20) NOT NULL,
    `assoc_type_id` bigint(20) NOT NULL,
    PRIMARY KEY `ampk` (`source_prop_type_id`, `target_prop_type_id`, `assoc_type_id`),
    CONSTRAINT `fk_mapping_source` FOREIGN KEY (`source_prop_type_id`) REFERENCES `property_types` (`id`),
    CONSTRAINT `fk_mapping_target` FOREIGN KEY (`target_prop_type_id`) REFERENCES `property_types` (`id`),
    CONSTRAINT `fk_mapping_assoc` FOREIGN KEY (`assoc_type_id`) REFERENCES `assoc_types` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;