import json
import csv
import re
import time
import datetime
import logging
from backbone_server.dao.base_dao import BaseDAO
from backbone_server.dao.entity_dao import EntityDAO
from backbone_server.dao.association_dao import AssociationDAO
from backbone_server.dao.model.server_property import ServerProperty
from backbone_server.dao.model.association_type import AssociationType
from backbone_server.errors.incomplete_combination_key_exception import IncompleteCombinationKeyException
from backbone_server.errors.no_id_exception import NoIdException
from backbone_server.errors.duplicate_id_exception import DuplicateIdException
from backbone_server.errors.invalid_id_exception import InvalidIdException
from backbone_server.errors.invalid_date_format_exception import InvalidDateFormatException
from backbone_server.errors.invalid_data_value_exception import InvalidDataValueException
from swagger_server.models.source_entity import SourceEntity
from swagger_server.models.summary_item import SummaryItem
from swagger_server.models.upload_response import UploadResponse

class SourceDAO(EntityDAO):

    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(__name__)

    def load_data_file(self, source, data_def, filename):

        input_stream = open('example.csv')

        return self.load_data(source, data_def, input_stream)

#https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html
    def load_data(self, source, data_def, input_stream, skip_header, update_only, entity_type):

        response = UploadResponse(0,0,0)


        with input_stream as csvfile:
            data_reader = csv.reader(csvfile, delimiter='\t')

            if skip_header:
                next(data_reader)

            self._connection = self.get_connection()
            self._cursor = self._connection.cursor()
            for row in data_reader:
                entity_id = None
                values = []
                prop_by_column = {}
                response.processed = response.processed + 1
                for name, defn in data_def['values'].items():
                    identity = False
                    if 'id' in defn and defn['id']:
                        identity = True
                    #Done here for efficiency
                    if 'type_id' not in defn:
                        prop_type = self.find_or_create_prop_defn(source, name, defn['type'],
                                                                  identity, defn['column'], True)
                        defn['type_id'] = prop_type.ident
                        defn['ptype'] = prop_type
                    #print(repr(defn))
                    #print(repr(row))
                    prop_by_column[defn['column']] = defn['ptype']
                    data_value = row[defn['column']]
                    data = ServerProperty(name, defn['type'], data_value, source, identity)
                    #Convert data value - make sure you set data_value
                    try:
                        if 'regex' in defn:
                            re_match = re.search(defn['regex'], data_value)
                            if re_match:
                                #print("Groupdict:" + repr(re_match.groupdict()))
                                try:
                                    data_value = re_match.group(1)
                                except IndexError as iere:
                                        raise InvalidDataValueException("Failed to parse {} using {}"
                                                                        .format(data_value, defn['regex'])) from iere
                                #print("Transformed value is:" + data_value + " from " + row[defn['column']])
                                #print(repr(re_match.groupdict()))
                                #if row[defn['column']] != "" and data_value == "":
                                #    print("Empty match: {} {}".format(defn['regex'], row[defn['column']]))
                            #else:
                            #    print("No match: {} {}".format(defn['regex'], data_value))
                        if defn['type'] == 'datetime':
                            date_format = data.default_date_format
                            try:
                                if not (data_value == '' or data_value == 'NULL'):
                                    if 'date_format' in defn:
                                        try:
                                            date_format = defn['date_format']
                                            data_value = datetime.datetime(*(time.strptime(data_value, date_format))[:6])
                                        except ValueError as dpe:
                                            raise InvalidDateFormatException("Failed to parse date '{}' using {}".format(data_value, date_format)) from dpe
                                    else:
                                        #To make sure that the default conversion works
                                        data.typed_data_value
                                else:
                                    #Skip this property
                                    continue
                            except (InvalidDataValueException,InvalidDateFormatException) as idfe:

                                self._connection.rollback()

                                self._cursor.close()
                                self._connection.close()
                                raise
                        if 'replace' in defn:
                            for subs in defn['replace']:
                                data_value = re.sub(subs[0], subs[1], data_value)
                                #print("Transformed value is:" + data_value + " from " + row[defn['column']])

                        #Reset data_value in data after any conversions
                        data.data_value = data_value

                    except IndexError:
                        self._logger.critical(repr(defn))
                        self._logger.critical(repr(row))
                        raise


                    data.type_id = defn['type_id']
                    values.append(data)

                if entity_type:
                    data = ServerProperty('entity_type', 'string', entity_type, 'system', False)
                    values.append(data)

                assoc_dao = AssociationDAO(self._cursor)

                #All we are doing here is to create mappings for implied foreign keys
                if 'refs' in data_def:
                    for name, defn in data_def['refs'].items():
                        fk_name = name
                        if 'fk_name' in defn:
                            fk_name = defn['fk_name']
                        if 'type_id' not in defn:
                            prop_type = self.find_or_create_prop_defn(defn['source'], fk_name, defn['type'], True, 0, False)
                            defn['type_id'] = prop_type.ident
                        if 'assoc_type' not in defn:
                            ref_type = None
                            if 'ref_type' in defn:
                                ref_type = defn['ref_type']
                            assoc_type = AssociationType(assoc_type=ref_type)
                            assoc_type.source = source
                            assoc_type.target = defn['source']
                            assoc_type.key = name
                            defn['assoc_type'] = self.find_or_create_assoc_type(assoc_type)
                            assoc_dao.create_mapping(defn['type_id'], prop_by_column[defn['column']].ident, defn['assoc_type'])

                record = SourceEntity()
                record.values = values
                entity_id, exists, modified = self.edit_source(record, update_only)

                if not exists and entity_id is not None:
                    response.created = response.created + 1
                elif modified:
                    response.modified = response.modified + 1

                #print("Entity_ID:" + str(entity_id))
                self.update_associations(entity_id, [])

            self._connection.commit()
            self._cursor.close()
            self._connection.close()

            return response

    def edit_source(self, source_rec, update_only):

        entity_id = None
        id_prop = None

        id_properties = []
        for prop in source_rec.values:
            if not isinstance(prop, ServerProperty):
                sprop = ServerProperty(prop.data_name, prop.data_type, prop.data_value,
                                       prop.source, prop.identity)
                prop = sprop
            if not prop.type_id:
                prop_type = self.find_or_create_prop_defn(prop.source, prop.data_name,
                                                          prop.data_type, prop.identity, 0,
                                                          True)
                prop.type_id = prop_type.ident

            if prop.identity:
                id_properties.append(prop)
                if prop.typed_data_value is None or (prop.data_type == 'string' and prop.data_value == ''):
                    self._logger.error("No key value:" + repr(prop))
#                print (repr(prop))


        entity_id, found = self.find_entity(id_properties)

        if not found:
            if update_only:
                self._logger.debug("No entity:" + repr(id_properties))
                entity_id, found = self.find_entity_by_fk(id_properties[0])
                if not found:
                    self._logger.debug("Still no entity:" + repr(id_properties))
                    return None, False, False
            else:
                entity_id = self.create_entity()

        self._logger.debug("Saving entity:" + str(entity_id))

        modified = self.save_entity(entity_id, source_rec, False)

        return entity_id, found, modified


    def fetch_entity_by_source(self, source, source_id):

        connection = self.get_connection()
        cursor = connection.cursor()
        prop_query = ("SELECT id, prop_type FROM property_types WHERE source = %s AND identity = true")
        cursor.execute(prop_query, (source,))

        result = cursor.fetchone()

        if not result:
            cursor.close()
            connection.close()
            raise InvalidIdException("No identity properties for :" + source)

        res = cursor.fetchone()
        if res:
            self._logger.error(source + ''' uses a combination key and can't be retrieved by this method ''' + repr(result) + repr(res))
            cursor.close()
            connection.close()
            raise IncompleteCombinationKeyException("Cannot fetch record with only one part of a combination key")

        prop_type_id = result[0]
        prop_type = result[1]

        if self._postgres:
            data_field = self.get_data_field(prop_type)
        else:
            data_field = self.get_data_field(BaseDAO._decode(prop_type))

        if self._postgres:
            sel = 'SELECT e.id'
        else:
            sel = 'SELECT HEX(e.id)'
        entity_query = sel + ''', ep.entity_id
            FROM
                properties p
            JOIN property_types pt
                ON pt.id = p.prop_type_id AND pt.identity = true
            JOIN entity_properties ep ON ep.property_id = p.id
            JOIN entities e ON e.added_id = ep.entity_id
            WHERE ''' + data_field + " = %s AND p.prop_type_id = %s"

        cursor.execute(entity_query, (source_id, prop_type_id))
        entity = cursor.fetchone()

        if not entity:
            cursor.close()
            connection.close()
            raise InvalidIdException("No record found for: {} {}".format(source, source_id))

        entity_id = str(entity[0])
        added_id = entity[1]

        cursor.close()
        connection.close()

        return self.fetch_entity_by_id(entity_id, added_id)

    def create_source_entity(self, source, entity):

        id_found = False
        id_props = []
        for prop in entity.values:
            if prop.identity:
                if prop.source == source:
                    id_found = True
                    id_props.append(prop)
                else:
                    raise InvalidIdException("Id for a difference source specified:" + source + ":" + repr(entity))

        if not id_found:
            raise NoIdException("No identity value specified:" + source + ":" + repr(entity))

        self._connection = self.get_connection()
        self._cursor = self._connection.cursor()

        existing_entity = self.find_entity_by_properties(id_props)
        if existing_entity:
            self._cursor.close()
            self._connection.close()
            raise DuplicateIdException("Duplicate identity value specified:" + source + ":" + repr(entity))

        entity_id = self.edit_source(entity, False)
        self._connection.commit()
        self._cursor.close()
        self._connection.close()

        return entity_id


    def get_report_count_by_source(self):

        query = '''SELECT DISTINCT count(ep.property_id), pt.source from entity_properties ep
                    JOIN properties p ON p.id = ep.property_id
                    JOIN property_types pt ON pt.id = p.prop_type_id AND pt.identity = true
                    GROUP BY pt.source, pt.id;'''
        self._connection = self.get_connection()
        self._cursor = self._connection.cursor()

        self._cursor.execute(query)

        results = []
        for (count, source) in self._cursor:
            summ = SummaryItem()
            summ.source_name = BaseDAO._decode(source)
            summ.num_items = count
            results.append(summ)

        self._connection.commit()
        self._cursor.close()
        self._connection.close()

        #print(repr(results))
        return results

if __name__ == '__main__':
    sd = SourceDAO()
    data_def = json.loads('{ "refs": { "oxf_code": { "column": 1, "type": "string", "source": "lims" }}, "values":{ "id": { "column": 24, "type": "integer", "id": true }, "sample_type": { "column": 6, "type": "string" } } }')
    sd.load_data_file('test', data_def, "example.csv")

    #print(repr(sd.fetch_entity_by_source('test',1)))
