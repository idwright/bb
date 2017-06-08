import json
import csv
#from base_dao import base_dao
from backbone_server.dao.base_dao import base_dao
from backbone_server.dao.entity_dao import entity_dao
from backbone_server.dao.model.bulk_load_property import BulkLoadProperty
from swagger_server.models.entity import Entity
from swagger_server.models.property import Property
from swagger_server.models.summary_item import SummaryItem
import binascii
import uuid
import mysql.connector
from mysql.connector import errorcode

class source_dao(entity_dao):

    _connection = None
    _cursor = None

    def load_data_file(self, source, data_def, filename):

        input_stream = open('example.csv')

        return self.load_data(source,data_def, input_stream)

#https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html
    def load_data(self, source, data_def, input_stream):

        with input_stream as csvfile:
            has_header = csv.Sniffer().has_header(csvfile.read(1024))
            csvfile.seek(0)
            data_reader = csv.reader(csvfile, delimiter = '\t')
            if has_header:
                next(data_reader)

            self._connection = self.get_connection()
            self._cursor = self._connection.cursor()
            for row in data_reader:
                entity_id = None
                values = []
                for name, defn in data_def['values'].items():
                    identity = False
                    if 'id' in defn and defn['id']:
                        identity = True
                    #Done here for efficiency
                    if not 'type_id' in defn:
                        defn['type_id'] = self.find_or_create_prop_defn(source, name, defn['type'], identity)
                    #print(repr(defn))
                    #print(repr(row))
                    data = BulkLoadProperty(name, defn['type'], row[defn['column']], source, identity)
                    data.type_id = defn['type_id']
                    values.append(data)

                refs = []
                if 'refs' in data_def:
                    for name, defn in data_def['refs'].items():
                        fk_name = name
                        if 'fk_name' in defn:
                            fk_name = defn['fk_name']
                        if not 'type_id' in defn:
                            defn['type_id'] = self.find_or_create_prop_defn(defn['source'], fk_name, defn['type'], True)
                        if not 'assoc_type_id' in defn:
                            defn['assoc_type_id'], assoc_name = self.find_or_create_assoc_defn(source, defn['source'], name)
                        data = {
                            'data_value': row[defn['column']],
                            'data_type': defn['type'],
                            'type_id': defn['type_id'],
                            'data_name': name,
                            'source': defn['source'],
                            'assoc_type_id': defn['assoc_type_id'],
                            'fk_name': defn['fk_name'] if 'fk_name' in defn else None
                        }
                        refs.append(data)

                record = { 'values': values, 'refs': refs}
                self.edit_source(record)
                self._connection.commit()
            self._cursor.close()
            self._connection.close()

    def edit_source(self, source_rec):

        system_fk_type_id = self.find_or_create_prop_defn('system', 'implied_id', 'boolean', False)
        system_fk_data = BulkLoadProperty('implied_id', 'boolean', 'false', 'system', False)
        system_fk_data.type_id = system_fk_type_id

        entity_id = None
        id_prop = None

        id_properties = []
        for prop in source_rec['values']:
            if type(prop) == 'BulkLoadProperty':
                if not prop.type_id:
                    prop.type_id = self.find_or_create_prop_defn(prop.source, prop.data_name, prop.data_type, prop.identity)

            if prop.identity:
                id_properties.append(prop)
#                print (repr(prop))


        entity_id, found = self.find_entity(id_properties)
        system_fk_data.data_value = 'false'
        id_prop = prop
        self.add_entity_property(entity_id, system_fk_data, system_fk_type_id)

        if entity_id:
            for prop in source_rec['values']:
                self.add_entity_property(entity_id, prop, prop.type_id)
        else:
             self._logger.critical("Missing id for %s", repr(source_rec), exc_info=1)
             return None

        #print("Identity property:" + repr(id_prop))
        if 'refs' in source_rec:
            for assoc in source_rec['refs']:
                if 'fk_name' in assoc and assoc['fk_name']:
                    fk_name = assoc['fk_name']
                else:
                    fk_name = assoc['data_name']
                if not 'type_id' in assoc:
                    assoc['type_id'] = self.find_or_create_prop_defn(assoc['source'], fk_name, assoc['data_type'], True)
                if not 'assoc_type_id' in assoc:
                    assoc['assoc_type_id'], assoc_name = self.find_or_create_assoc_defn(source, assoc['source'], assoc['data_name'])
                fk = None
                if not assoc['data_value'] or assoc['data_value'].lower() == "null":
                    continue
                fk_prop = BulkLoadProperty(fk_name, assoc['data_type'], assoc['data_value'], assoc['source'], False)
                if not found:
                    fk, found = self.find_entity([ fk_prop ])
                if not found:
                    system_fk_data.data_value = "true"
                    self.add_entity_property(fk, system_fk_data, system_fk_type_id)
                    self.add_entity_property(fk, fk_prop, assoc['type_id'])
                self.add_assoc(fk, entity_id, assoc['assoc_type_id'])
                if 'values' in source_rec['refs']:
                    for prop in source_rec['refs']['values']:
                        if not 'type_id' in prop:
                            prop['type_id'] = self.find_or_create_prop_defn(assoc_name, prop['data_name'], prop['data_type'], False)
                        self.add_assoc_property(entity_id, fk, assoc['assoc_type_id'], prop, prop['type_id'])

        return entity_id


    def fetch_entity_by_source(self, source, source_id):

        connection = self.get_connection()
        cursor = connection.cursor()
        prop_query = ("SELECT id, prop_type FROM property_types WHERE source = %s AND identity = 1")
        cursor.execute(prop_query, (source,))

        result = cursor.fetchone()

        if not result:
            cursor.close()
            connection.close()
            return None

        prop_type_id = result[0]
        prop_type = result[1]

        data_field = self.get_data_field(prop_type)

        entity_query = '''SELECT
            HEX(e.id), ep.entity_id
            FROM
                properties p
            JOIN property_types pt
                ON pt.id = p.prop_type_id AND pt.identity = 1
            JOIN entity_properties ep ON ep.property_id = p.id
            JOIN entities e ON e.added_id = ep.entity_id
            WHERE `''' + data_field + "` = %s AND p.prop_type_id = %s"

        cursor.execute(entity_query, (source_id,prop_type_id))
        entity = cursor.fetchone()

        if not entity:
            cursor.close()
            connection.close()
            return None

        entity_id = entity[0]
        added_id = entity[1]

        cursor.close()
        connection.close()

        return self.fetch_entity_by_id(entity_id, added_id)

    def update_source_entity(self, source, source_id, entity):

        id_found = False
        for prop in entity['values']:
            if 'identity' in prop and prop['identity']:
                id_found = True

        if not id_found:
            existing_entity = self.fetch_entity_by_source(source,source_id)
            for prop in existing_entity['values']:
                if 'identity' in prop and prop['identity']:
                    entity['values'].append(prop)

        self._connection = self.get_connection()
        self._cursor = self._connection.cursor()
        entity_id = self.edit_source(entity)
        self._connection.commit()
        self._cursor.close()
        self._connection.close()

        return entity_id

    def create_source_entity(self, source, entity):

        id_found = False
        id_prop = None
        for prop in entity['values']:
            if 'identity' in prop and prop['identity']:
                id_found = True
                id_prop = prop

        if not id_found:
            self._logger.error("No identity value specified:" + source + ":" + repr(entity))
            #Throw no id specified exception
            return None
        else:
            existing_entity = self.fetch_entity_by_source(source,id_prop['data_value'])
            if existing_entity:
                self._logger.error("Duplicate identity value specified:" + source + ":" + repr(entity))
                #Throw no id specified exception
                return None



        self._connection = self.get_connection()
        self._cursor = self._connection.cursor()
        entity_id = self.edit_source(entity)
        self._connection.commit()
        self._cursor.close()
        self._connection.close()

        return entity_id

    def get_summary_by_property(self, source, prop_name, threshold):

        th = 0
        if threshold:
            th = threshold

        self._connection = self.get_connection()
        self._cursor = self._connection.cursor()

        q= ("SELECT id, prop_type FROM `property_types` WHERE `source` = %s AND `prop_name` = %s")
        self._cursor.execute(q, (source, prop_name,))

        property_type_id = None
        property_type = None
        for (pti,pt) in self._cursor:
            property_type_id = pti
            property_type = pt

        query = ('''SELECT count(ep.property_id), pt.`source`, pt.prop_name, pt.prop_type, p.''' + self.get_data_field(property_type) +
                ''' from entity_properties ep
            JOIN properties p ON p.id = ep.property_id
            JOIN property_types pt ON pt.id = p.prop_type_id
            WHERE `pt`.`source` = %s AND `pt`.`prop_name` = %s
            GROUP BY (ep.property_id) HAVING COUNT(ep.property_id) > %s order by prop_name, ''' +
                 self.get_data_field(property_type))


        self._cursor.execute(query, (source, prop_name, th))

        results = []
        for (count, source, pname, ptype, pvalue) in self._cursor:
            summ = SummaryItem()
            summ.source_name = pvalue
            summ.num_items = count
            results.append(summ)

        self._connection.commit()
        self._cursor.close()
        self._connection.close()

        return results

    def get_source_properties(self, source):

        query = '''SELECT COUNT(pt.prop_name), pt.prop_name from property_types pt
            JOIN properties p ON p.prop_type_id = pt.id
                WHERE `pt`.source = %s
                    GROUP BY (pt.prop_name);'''

        self._connection = self.get_connection()
        self._cursor = self._connection.cursor()

        self._cursor.execute(query, (source,))

        results = []
        for (count, pname) in self._cursor:
            summ = SummaryItem()
            summ.source_name = pname
            summ.num_items = count
            results.append(summ)

        self._connection.commit()
        self._cursor.close()
        self._connection.close()

        return results

    def get_report_count_by_source(self):

        query = '''SELECT DISTINCT count(ep.property_id), `pt`.`source` from entity_properties ep
                    JOIN properties p ON p.id = ep.property_id
                    JOIN property_types pt ON pt.id = p.prop_type_id AND pt.identity = 1
                    GROUP BY `pt`.`source`, pt.id;'''
        self._connection = self.get_connection()
        self._cursor = self._connection.cursor()

        self._cursor.execute(query)

        results = []
        for (count, source) in self._cursor:
            summ = SummaryItem()
            summ.source_name = source
            summ.num_items = count
            results.append(summ)

        self._connection.commit()
        self._cursor.close()
        self._connection.close()

        #print(repr(results))
        return results

if __name__ == '__main__':
    sd = source_dao()
    data_def = json.loads('{ "refs": { "oxf_code": { "column": 1, "type": "string", "source": "lims" }}, "values":{ "id": { "column": 24, "type": "integer", "id": true }, "sample_type": { "column": 6, "type": "string" } } }')
    sd.load_data_file('test', data_def, "example.csv")

    #print(repr(sd.fetch_entity_by_source('test',1)))
