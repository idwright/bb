from backbone_server.dao.base_dao import BaseDAO
from backbone_server.dao.model.server_property import ServerProperty
from backbone_server.dao.model.server_relationship import ServerRelationship
from backbone_server.errors.invalid_data_value_exception import InvalidDataValueException
import mysql.connector
from mysql.connector import errorcode

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


    def merge_implied_associations(self, internal_id):

        query = '''SELECT ia.source_id, ia.target_id, ia.assoc_type_id, string_value, long_value, target_prop_id 
            FROM implied_assocs ia
            LEFT JOIN entity_assoc ea ON ia.target_id = ea.target_entity_id AND ia.source_id =
            ea.source_entity_id AND ia.assoc_type_id = ea.assoc_type_id
                WHERE ia.assoc_type = %s AND ea.source_entity_id IS NULL AND target_prop_id IN (SELECT 
            property_id
        FROM
            entity_properties
        WHERE
            entity_id = %s);'''

        self._cursor.execute(query, ('sibling', internal_id,))

        merges = []
        string_val = None
        long_val = None
        target_prop_id = None
        for (sid, tid, ati, spv, lpv, tpi) in self._cursor:
            if sid != tid:
                if spv:
                    string_val = spv.decode('utf-8')
                long_val = lpv
                target_prop_id = tpi
                srel = ServerRelationship()
                srel.source_id = sid
                srel.target_id = tid
                merges.append(srel)

        merge_query = '''UPDATE `entity_properties` SET entity_id = %s WHERE entity_id = %s'''
        merge_assoc_query = '''UPDATE `entity_assoc` ea
        INNER JOIN
    `assoc_properties` ap ON (ea.source_entity_id = ap.source_entity_id
        AND ea.target_entity_id = ap.target_entity_id
        AND ea.assoc_type_id = ap.assoc_type_id)
SET
    ea.target_entity_id = %s,
    ap.target_entity_id = %s
WHERE
    ap.target_entity_id = %s;'''

        delete_system_query = '''DELETE FROM entity_properties
                                        WHERE
                                            entity_id = %s
                                            AND property_id IN (SELECT
                                                p.id
                                            FROM
                                                properties p
                                                    JOIN
                                                property_types pt ON p.prop_type_id = pt.id
                                            WHERE
                                                pt.`source` = 'system');'''
        delete_query = '''DELETE FROM `entities` WHERE added_id = %s'''

        duplicate_query = '''
SELECT 
    DISTINCT property_id
FROM
    property_values
WHERE
     property_id IN (SELECT 
            property_id
        FROM
            property_values
        WHERE
            added_id IN (%s,%s)
        GROUP BY property_id
        HAVING COUNT(*) > 1)
        '''

        for srel in merges:
            try:
            #Delete any that might cause duplicate entries (e.g. system implied_id true)
                self._cursor.execute(query, (srel.source_id, srel.target_id))

                dups = []
                for (prop_id) in self._cursor:
                    dups.append(prop_id)

                for (prop_id) in dups:
                    self._cursor.execute("DELETE FROM entity_properties WHERE entity_id = %s AND property_id = %s", (srel.target_id, prop_id))

#            print("Merge {} {}".format(srel.source_id, srel.target_id))
                self._cursor.execute(delete_system_query, (srel.target_id,))

                self._cursor.execute(merge_query, (srel.source_id, srel.target_id))

#            print("Merge assoc:" + merge_assoc_query %
#                                 (srel.target_id, srel.target_id, srel.source_id))
                self._cursor.execute('SET foreign_key_checks = 0')
                self._cursor.execute(merge_assoc_query,
                                     (srel.target_id, srel.target_id, srel.source_id))
                self._cursor.execute('SET foreign_key_checks = 1')
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_DUP_ENTRY:
                    print("Error creating implied_association {} {}".format(internal_id, merge_query % (srel.source_id, srel.target_id)))
                    print("Prop id:" + str(target_prop_id) + " values:" + string_val + ", " + str(long_val))
                    raise InvalidDataValueException("Error creating implied_association for {} - {}".
                                                    format(internal_id, merge_query % (srel.source_id, srel.target_id))) from err


#            print(delete_query % srel.target_id)
#            self._cursor.execute(delete_query, (srel.target_id,))


    def create_implied_associations(self, internal_id):

        query = '''INSERT INTO entity_assoc (source_entity_id, target_entity_id, assoc_type_id)
        select ia.source_id, ia.target_id, ia.assoc_type_id FROM implied_assocs ia
            LEFT JOIN entity_assoc ea ON ia.target_id = ea.target_entity_id AND ia.source_id =
            ea.source_entity_id AND ia.assoc_type_id = ea.assoc_type_id
                WHERE ia.assoc_type = %s AND ea.source_entity_id IS NULL AND target_prop_id IN (SELECT 
            property_id
        FROM
            entity_properties
        WHERE
            entity_id = %s);'''

        self._cursor.execute(query, ('parent-child', internal_id,))


    def find_missing_association_sources(self, internal_id):

        query = '''SELECT source_prop_type_id, ims.`source`, ims.prop_name, ims.prop_type,
        ims.string_value, ims.long_value
                    FROM implied_sources ims WHERE target_prop_id IN (SELECT property_id from
                    entity_properties where entity_id = %s);'''

        missing_properties = []

        self._cursor.execute(query, (internal_id,))

        for (spti, source, prop_name, prop_type, string_val, long_val) in self._cursor:
            #print("{} {} {} {}".format(spti, source, pt, val))
            prop = ServerProperty()
            prop.type_id = spti
            prop.source = source.decode('utf-8')
            prop.data_type = prop_type.decode('utf-8')
            prop.data_name = prop_name.decode('utf-8')
            prop.identity = True
            if prop.data_type == 'string':
                prop.data_value = string_val.decode('utf-8')
                if prop.data_value == '':
                    continue
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
