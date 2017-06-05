import json
import csv
#from base_dao import base_dao
from backbone_server.dao.base_dao import base_dao
from swagger_server.models.entity import Entity
from swagger_server.models.property import Property
from swagger_server.models.relationship import Relationship
from typing import List, Dict
import binascii
import uuid
import mysql.connector
from mysql.connector import errorcode
import datetime

class entity_dao(base_dao):

    _connection = None
    _cursor = None

    """
        updates an entity

        :param entity:
        :type entity: Entity

        :rtype: Entity
    """
    def update_entity(self, entity):

        self._connection = self.get_connection()
        self._cursor = self._connection.cursor()

        internal_id = self.get_internal_id(entity.entity_id)

        for prop in entity.values:
            property_type_id = self.find_or_create_prop_defn(prop.source, prop.data_name, prop.data_type, prop.identity)
            self.add_entity_property(internal_id, prop, property_type_id)

        if entity.refs:
            for assoc in entity.refs:
                assoc_type_id = self.find_or_create_assoc_type(assoc.assoc_name)
                internal_target_id = self.get_internal_id(assoc.target_id)
                self.add_assoc(internal_id, internal_target_id, assoc_type_id)
                if assoc.values:
                    for prop in assoc.values:
                        property_type_id = self.find_or_create_prop_defn(prop.source, prop.data_name, prop.data_type, prop.identity)
                        self.add_assoc_property(internal_id, internal_target_id, assoc['assoc_type_id'], prop, property_type_id)


        retval = self.get_entity_by_id(entity.entity_id, internal_id)
        self._connection.commit()
        self._cursor.close()
        self._connection.close()


        return retval

    def find_or_create_assoc_defn(self, source, target, key):
        assoc_name = key + "_" + source + "_" + target
#        cnx = self.get_connection()
#        cursor = cnx.cursor()
        return self.find_or_create_assoc_type(assoc_name)

    def find_or_create_assoc_type(self, assoc_name):

        self._cursor.execute("SELECT id FROM `assoc_types` WHERE `assoc_name` = %s", (assoc_name,))

        assoc_type_id = None
        for (pti) in self._cursor:
            assoc_type_id = pti[0]

        if not assoc_type_id:
            self._cursor.execute("INSERT INTO `assoc_types` (`assoc_name`) VALUES (%s)", (assoc_name,))
            assoc_type_id = self._cursor.lastrowid
#            cnx.commit()
#        cursor.close()
#        cnx.close()

        return assoc_type_id, assoc_name

    def find_or_create_prop_defn(self, source, name, data_type, identity):
#        cnx = self.get_connection()
#        cursor = cnx.cursor()

        self._cursor.execute("SELECT id FROM `property_types` WHERE `source` = %s AND `prop_name` = %s AND `prop_type` = %s", (source, name, data_type))

        property_type_id = None
        for (pti,) in self._cursor:
            property_type_id = pti

        if not property_type_id:
            self._cursor.execute("INSERT INTO `property_types` (`source`, `prop_name`, `prop_type`, `identity`) VALUES (%s, %s, %s, %s)", (source, name, data_type, identity))
            property_type_id = self._cursor.lastrowid
            #cnx.commit()
#        cursor.close()
#        cnx.close()

        return property_type_id

    """
        adds a Property to an entity

        :param prop:
        :type prop: Property

        :rtype: None
    """
    def add_or_update_property_entity(self, entity_id, prop, property_type_id):

        data_field = self.get_data_field(prop.data_type)

        fetch_row = ("SELECT HEX(e.id),e.added_id, p.id as property_id, " + data_field + " FROM `properties` p LEFT JOIN `property_types` AS pt ON pt.id = p.prop_type_id JOIN `entity_properties` AS ep ON ep.property_id = p.id LEFT JOIN `entities` AS e ON ep.entity_id = e.added_id WHERE `pt`.`prop_name` = %s AND `source`=%s AND `added_id` = %s")

        self._cursor.execute(fetch_row, (prop.data_name, prop.source, entity_id))
        property_id = None
        old_value = None

        #print (fetch_row)
        #print ((prop['data_name'], prop['source'], entity_id))
        prop_matched_id = None
        for (ent_id, added_id, prop_id, old_val) in self._cursor:
            #print ("comparing: " + str(old_val) + " vs " + str(self.get_prop_value(prop)))
            #print ("comparing types: " + str(type(old_val)) + " vs " + str(type(self.get_prop_value(prop))))
            if old_val == self.get_prop_value(prop):
        #        print ("match")
                prop_matched_id = prop_id
                return prop_id, False, None, False, True
            else:
                old_value = old_val
                property_id = prop_id

#        cursor.close()
#        cnx.close()
        return self.insert_or_update_property(prop, property_type_id, data_field, property_id, old_value)


    """
        adds a Property to an entity

        :param prop:
        :type prop: Property

        :rtype: None
    """
    def add_entity_property(self, entity_id, prop, property_type_id):
#        print("Add entity_property:" + str(entity_id) + " " + source + " " + repr(prop))
        property_id, create, delete_old, exists, linked = self.add_or_update_property_entity(entity_id, prop, property_type_id)

        #print("add_entity_property:" + str(property_id) + str(create) + str(delete_old) + str(exists))
        if delete_old:
            old_property_id = delete_old
            #Note - do not delete the old property, intended to be used for history
#            print ("Delete reference to old property value:" + str(entity_id) + ":" + str(old_property_id))
            self._cursor.execute("DELETE FROM `entity_properties` WHERE `entity_id` = %s AND `property_id` = %s", (entity_id, old_property_id))
        if not linked:
            self._cursor.execute("INSERT INTO `entity_properties` (`entity_id`, `property_id`) VALUES (%s, %s)", (entity_id, property_id))

    def get_data_field(self, data_type):
        data_field = {
            'string': "string_value",
            'integer': "long_value",
            'float': "float_value",
            'double': "double_value",
            'json': "json_value",
            'boolean': "boolean_value",
            'datetime': "string_value",
        }.get(data_type, 'string_value')

        return data_field

    def get_data_value(self, data_type, data_value):
        converted_field = {
            'string': lambda x: x,
            'integer': lambda x: None if x.lower() == "null" or x == '' else int(x),
            'float': lambda x: float(x),
            'double': lambda x: float(x),
            'json': lambda x: x,
            'boolean': lambda x: 1 if x.lower() == 'true' else 0,
            'datetime': lambda x: x,
            }.get(data_type)(data_value)

        return converted_field

    def get_prop_value(self, prop):

        return self.get_data_value(prop.data_type, prop.data_value)

    def add_or_update_assoc_property(self, entity_id, fk, assoc_type_id, source, prop):

        data_field = self.get_data_field(prop['data_type'])

        fetch_row = ("SELECT HEX(e.id),e.added_id, p.id as property_id, " + data_field + " FROM `properties` p LEFT JOIN `property_types` AS pt ON pt.id = p.prop_type_id LEFT JOIN `assoc_properties` AS ap ON ap.property_id = p.id LEFT JOIN `entities` AS e ON ep.entity_id = e.added_id WHERE `pt`.`prop_name` = %s AND `source`=%s AND `source_entity_id` = %s AND `target_entity_id` = %s AND `assoc_type_id` = %s")


        self._cursor.execute(fetch_row, (prop['data_name'], prop['source'], entity_id, fk, assoc_type_id))
        property_details = []
        for (entity_id, added_id, prop_id, value) in self._cursor:
            property_details.append({ 'entity_id': entity_id, 'property_id': prop_id, 'value': value , 'added_id': added_id})

        return self.insert_or_update_property(property_details, prop, data_field)

    """
        adds or updates a Property

        :param prop:
        :type prop: Property
        :param data_field: which data field the value is held in
        :param property_id: the id of an existing property which matches prop
        :type property_id: int
        :param old_value: the current value in property_id
        :return: property_id, created, multiple_values, updated, matched

        :rtype: None
    """
    def insert_or_update_property(self, prop, property_type_id, data_field, property_id, old_value):

        #print("insert_or_update_property:" + str(data_field) + " property_id:" + str(property_id))
        #print("insert_or_update_property old_value:" + str(old_value) + " type:" + str(type(old_value)))
        self._logger.debug("insert_or_update_property:" + repr(prop))
        multiple_values = False

        if property_id and old_value:
            #Need to check if there are other entities referencing the same property before updating
            count_query = ("SELECT p.id FROM `properties` p LEFT JOIN `entity_properties` AS ep ON ep.property_id = p.id LEFT JOIN `assoc_properties` AS ap ON ap.property_id = p.id WHERE `" + data_field + "` = %s and p.id = %s LIMIT 5")

            self._cursor.execute(count_query, ( old_value, property_id))

            #Neither of these work
            #count = self._cursor.rowcount
            #results = self._connection.get_rows(count)
            #count = len(results)

            count = 0
            for (pid,) in self._cursor:
                count = count + 1
                pass
            #print(count_query)
            #print("count:" + str(count))
            if count == 1:
                #print ("insert_or_update_property: results == 1")
                if self.get_data_value(prop.data_type,old_value) != prop.data_value:
                    #Update property value
                    update_prop = ("UPDATE properties SET `" + data_field + "` = %s WHERE id = %s;")
                    self._cursor.execute(update_prop, (prop.data_value, property_id))
                return property_id, False, None, True, True
            elif count > 1:
                multiple_values = True
                #print ("insert_or_update_property: results > 1")
            else:
                pass
                #print ("insert_or_update_property: results " + repr(results))

        if not multiple_values:
            #print ("insert_or_update_property: not multiple_values")
            count_query = ("SELECT p.id FROM `properties` p JOIN `property_types` AS pt ON pt.id = p.prop_type_id WHERE `" + data_field + "` = %s AND `pt`.`source` = %s AND `pt`.`prop_name` = %s AND `pt`.`prop_type` = %s")

            #print(count_query)
            #print(repr(prop))
            self._cursor.execute(count_query, ( self.get_prop_value(prop), prop.source, prop.data_name, prop.data_type))

            existing_property_id = None
            for (prop_id,) in self._cursor:
                existing_property_id = prop_id

            if existing_property_id:
                #print("insert_or_update_property: existing property found")
                return existing_property_id, False, None, False, False

        #print ("insert_or_update_property: inserting")
        insert_statement = ("INSERT INTO properties (`prop_type_id`, `" + data_field + "`) VALUES (%s, %s);")

        #print(insert_statement)
        #print (repr(prop))
        self._cursor.execute(insert_statement, (property_type_id, self.get_prop_value(prop)))
        new_property_id = self._cursor.lastrowid
        #print ("Added property id:" + str(new_property_id) + repr(prop))

        return new_property_id, True, property_id, False, False

    def add_assoc_property(self, entity_id, fk, assoc_type_id, prop, property_type_id):

        property_id, create = self.add_or_update_assoc_property(entity_id, fk, assoc_type_id, prop, property_type_id)

        if create:
#            cnx = self.get_connection()
#            cursor = cnx.cursor()
            query = ("INSERT INTO `assoc_properties` (`source_entity_id`, `target_entity_id`, `assoc_type_id`, `property_id`) VALUES (%s, %s, %s, %s)")

            self._cursor.execute(query, (entity_id, fk, assoc_type_id, property_id))

#            cnx.commit()
#            cursor.close()
#            cnx.close()


    def find_entity_by_properties(self, properties):

        fetch_row = ('''SELECT
                        HEX(entity_id), added_id
                    FROM
                        `properties` p
                        JOIN property_types pt ON pt.id = p.prop_type_id
                        JOIN entity_properties ep ON ep.property_id = p.id
                        JOIN entities e ON e.added_id = ep.entity_id
                    WHERE ''')

        filters = []
        values = []
        for prop in properties:
            pfilter = '`prop_name` = %s AND `source` = %s'
            values.append(prop.data_name)
            values.append(prop.source)
            if prop.data_value:
                pfilter = pfilter + " AND `" + self.get_data_field(prop.data_type) +"` = %s"
                values.append(prop.data_value)
            filters.append(pfilter)

        fetch_row = fetch_row + ' AND '.join(filters)

        self._cursor.execute(fetch_row, values)


        property_details = []
        for (entity_id, added_id) in self._cursor:
            property_details.append({ 'entity_id': entity_id, 'added_id': added_id})
#        print(fetch_row)
#        print((prop_name, source, prop_value))
#        print (property_details)
#        cursor.close()
#        cnx.close()

        return property_details

    def find_entity(self, id_properties):

        found = False
        property_details = self.find_entity_by_properties(id_properties)

        #print(property_details)
        if len(property_details) == 1:
#            print ("Found entity:" + repr(property_details))
            parent_entity_id = property_details[0]['added_id']
            found = True
        elif len(property_details) > 1:
            self._logger.critical("Duplicate entities:" + source + " " + prop_name + " " + str(entity_id))
        else:
#            cnx = self.get_connection()
#            cursor = cnx.cursor()
            query = ("INSERT INTO `entities` (`id`) VALUES (ordered_uuid(uuid()))")
            args = ( )
            self._cursor.execute(query, args)
#            cnx.commit()
            parent_entity_id = self._cursor.lastrowid
#            print ("Added" + str(row_id))
#            cursor.execute("SELECT id FROM `entities` WHERE `added_id` = %s", (row_id,))
#            parent_entity_id = cursor.fetchone()[0]
#            print("inserted entity " + str(parent_entity_id))
#            cnx.commit()

#            cursor.close()
#            cnx.close()

        return parent_entity_id, found

    def add_assoc(self, entity_id, fk, assoc_type_id):
#        cnx = self.get_connection()
#        cursor = cnx.cursor()
        query = ("INSERT INTO `entity_assoc` (`source_entity_id`, `target_entity_id`, `assoc_type_id`) VALUES (%s, %s, %s)")
        args = (entity_id, fk, assoc_type_id)
#        print (query)
#        print (args)
        try:
            self._cursor.execute(query, args)
#            cnx.commit()
        except mysql.connector.Error as err:
            #https://github.com/mysql/mysql-connector-python/blob/master/lib/mysql/connector/errorcode.py
            if err.errno == errorcode.ER_DUP_ENTRY:
                #self._logger.warn("Updating existing assoc")
                pass
#        cursor.close()
#        cnx.close()


    def get_internal_id(self, entity_id):
        added_id = None

        added_id_query = 'SELECT added_id FROM entities WHERE id = UNHEX(%s);'
        self._cursor.execute(added_id_query, (entity_id,))
        res = self._cursor.fetchone()
        if res:
            added_id = res[0]

        return added_id

    def fetch_entity_by_id(self, entity_id, added_id):

        self._connection = self.get_connection()
        self._cursor = self._connection.cursor()

        retval = self.get_entity_by_id(entity_id, added_id)

        self._cursor.close()
        self._connection.close()

        return retval

    def get_entity_by_id(self, entity_id, added_id):
        if not added_id:
            added_id = self.get_internal_id(entity_id)

        entity = Entity(entity_id)
        props_query = 'SELECT `source`, `prop_name`, `prop_type`, `value`, `identity` FROM property_values WHERE `added_id` = %s'

        self._cursor.execute(props_query, (added_id,))

        properties = []
        for (source, prop_name, prop_type, value, identity) in self._cursor:
            data = Property()
            data.data_type = prop_type
            data.data_name = prop_name
            data.identity = bool(identity)
            data.source = source
            if value:
                data.data_value = value
            else:
                #print("Null value for:" + repr(data))
                pass
            properties.append(data)

        entity.values = properties
        assocs_query = '''SELECT source_uuid, source_id, target_uuid, target_id, assoc_name, assoc_type_id FROM `associations`
        WHERE source_id = %s OR target_id = %s;'''
        self._cursor.execute(assocs_query, (added_id, added_id,))
        links = []
        for assoc_data in self._cursor:
            links.append(assoc_data)

        refs = []
        for ad in links:
            sad = ad[1]
            tad = ad[3]
            assoc_name = ad[4]
            ati = ad[5]
            fetch_row = '''select `prop_name`, `prop_type`, `value`, `identity` from association_property_values
                            WHERE `source_id` = %s AND `target_id` = %s AND `assoc_type_id` = %s'''
            self._cursor.execute(fetch_row, (sad, tad, ati))
            values = []
            for (prop_name, prop_type, prop_value, identity) in self._cursor:
                value = {
                    'data_value': prop_value,
                    'data_type': prop_type,
                    'data_name': prop_name,
                    'identity': bool(identity),
                }
                values.append(value)
            data = {
                'source_id': ad[0],
                'target_id': ad[2],
                'assoc_name': assoc_name,
                'values': values
            }
            refs.append(data)


        entity.refs = refs
        #print ("Fetched entity:" + str(added_id))
        return entity


    def fetch_entities_by_property(self, prop_name, prop_value):

        self._connection = self.get_connection()
        self._cursor = self._connection.cursor()

        self._cursor.execute("SELECT id, prop_type FROM `property_types` WHERE `prop_name` = %s", (prop_name,))

        property_type_id = None
        property_type = None
        entities = []
        props = []
        for (pti,pt) in self._cursor:
            property_type_id = pti
            property_type = pt
            props.append({ 'pti': pti, 'pt': pt})

        for (prop) in props:
            props_query = '''SELECT
                HEX(e.id), e.added_id
                FROM
                    properties p
                LEFT JOIN entity_properties ep ON ep.property_id = p.id
                LEFT JOIN entities e ON e.added_id = ep.entity_id
                WHERE prop_type_id = %s AND ''' + self.get_data_field(prop['pt']) + ' = %s'

            try:
                query_value = self.get_data_value(prop['pt'], prop_value)
                #print(props_query)
                #print("{} {}".format(repr(prop), repr(query_value)))
                self._cursor.execute(props_query, (prop['pti'], query_value,))

                ents = []
                for (ent_id,added_id,) in self._cursor:
                    ents.append({ 'ent_id': ent_id, 'added_id': added_id})

                for ent in ents:
                    entities.append(self.get_entity_by_id(ent["ent_id"], ent["added_id"]))
            except ValueError:
                self._logger.warn("Mismatch type when searching: {} {} {}".format(prop_name, prop_value, repr(prop)))

        self._cursor.close()
        self._connection.close()

        return entities
#if __name__ == '__main__':
#    sd = source_dao()
#    data_def = json.loads('{ "refs": { "oxf_code": { "column": 1, "type": "string", "source": "lims" }}, "values":{ "id": { "column": 24, "type": "integer", "id": true }, "sample_type": { "column": 6, "type": "string" } } }')
#    sd.load_data('test', data_def)
#
#    print(repr(sd.fetch_entity_by_source('test',1)))
