from backbone_server.dao.base_dao import BaseDAO
from backbone_server.dao.model.bulk_load_property import BulkLoadProperty
from backbone_server.dao.model.server_relationship import ServerRelationship

class AssociationDAO(BaseDAO):

    def __init__(self, cursor):
        self._cursor = cursor


    def create_mapping(self, source_prop_id, target_prop_id, assoc_type):

        query = '''SELECT * FROM `assoc_mappings` WHERE source_prop_type_id = %s AND
        target_prop_type_id = %s AND assoc_type_id = %s'''

        self._cursor.execute(query, (source_prop_id, target_prop_id, assoc_type.ident))

        if not self._cursor.fetchone():
            query = '''INSERT INTO `assoc_mappings` (source_prop_type_id, target_prop_type_id,
            assoc_type_id) VALUES (%s, %s, %s)'''

            self._cursor.execute(query, (source_prop_id, target_prop_id, assoc_type.ident))


    def create_implied_associations(self, internal_id):

        query = '''INSERT INTO entity_assoc (source_entity_id, target_entity_id, assoc_type_id)
        select ia.source_id, ia.target_id, ia.assoc_type_id FROM implied_assocs ia
            LEFT JOIN entity_assoc ea ON ia.target_id = ea.target_entity_id AND ia.source_id =
            ea.source_entity_id AND ia.assoc_type_id = ea.assoc_type_id
                WHERE ea.source_entity_id IS NULL AND target_prop_id IN (SELECT 
            property_id
        FROM
            entity_properties
        WHERE
            entity_id = %s);'''

        self._cursor.execute(query, (internal_id,))


    def find_missing_association_sources(self, internal_id):

        query = '''SELECT source_prop_type_id, ims.`source`, ims.prop_name, ims.prop_type,
        ims.string_value, ims.long_value
                    FROM implied_sources ims WHERE target_prop_id IN (SELECT property_id from
                    entity_properties where entity_id = %s);'''

        missing_properties = []

        self._cursor.execute(query, (internal_id,))

        for (spti, source, prop_name, prop_type, string_val, long_val) in self._cursor:
            #print("{} {} {} {}".format(spti, source, pt, val))
            prop = BulkLoadProperty()
            prop.type_id = spti
            prop.source = source.decode('utf-8')
            prop.data_type = prop_type.decode('utf-8')
            prop.data_name = prop_name.decode('utf-8')
            prop.identity = True
            if prop.data_type == 'string':
                prop.data_value = string_val.decode('utf-8')
            elif prop.data_type == 'integer':
                prop.data_value = str(long_val)
            missing_properties.append(prop)

        return missing_properties

    def delete_implied_associations(self, internal_id):

        query = '''SELECT ea.source_entity_id, ea.target_entity_id, ea.assoc_type_id
                    FROM
                        entity_assoc ea
                            LEFT JOIN
                        implied_assocs ia ON ia.target_id = ea.target_entity_id
                            AND ia.source_id = ea.source_entity_id
                            AND ia.assoc_type_id = ea.assoc_type_id
                         JOIN
                            assoc_types asst ON asst.id = ea.assoc_type_id
                    WHERE
                    ia.source_id IS NULL AND (ea.target_entity_id = %s)'''

        self._cursor.execute(query, (internal_id, ))

        invalid_relationships = []
        for (seid, teid, atid) in self._cursor:
            #print((seid, teid, atid, asst))
            rel = ServerRelationship(source_id=seid, target_id=teid)
            rel.assoc_type_id = atid
            invalid_relationships.append(rel)

        for assoc in invalid_relationships:
            query = '''DELETE FROM assoc_properties
                    WHERE source_entity_id = %s AND target_entity_id = %s AND assoc_type_id = %s'''
            self._cursor.execute(query, (assoc.source_id, assoc.target_id, assoc.assoc_type_id))
            query = '''DELETE FROM entity_assoc
                    WHERE source_entity_id = %s AND target_entity_id = %s AND assoc_type_id = %s'''
            self._cursor.execute(query, (assoc.source_id, assoc.target_id, assoc.assoc_type_id))
