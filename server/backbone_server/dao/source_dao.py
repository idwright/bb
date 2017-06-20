import json
import csv
from backbone_server.dao.entity_dao import EntityDAO
from backbone_server.dao.association_dao import AssociationDAO
from backbone_server.dao.model.bulk_load_property import BulkLoadProperty
from backbone_server.errors.incomplete_combination_key_exception import IncompleteCombinationKeyException
from backbone_server.errors.no_id_exception import NoIdException
from backbone_server.errors.duplicate_id_exception import DuplicateIdException
from backbone_server.errors.invalid_id_exception import InvalidIdException
from swagger_server.models.source_entity import SourceEntity
from swagger_server.models.summary_item import SummaryItem

class SourceDAO(EntityDAO):

    def load_data_file(self, source, data_def, filename):

        input_stream = open('example.csv')

        return self.load_data(source, data_def, input_stream)

#https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html
    def load_data(self, source, data_def, input_stream):

        retcode = 200

        with input_stream as csvfile:
            has_header = csv.Sniffer().has_header(csvfile.read(1024))
            csvfile.seek(0)
            data_reader = csv.reader(csvfile, delimiter='\t')
            if has_header:
                next(data_reader)

            self._connection = self.get_connection()
            self._cursor = self._connection.cursor()
            for row in data_reader:
                entity_id = None
                values = []
                prop_by_column = {}
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
                    try:
                        data = BulkLoadProperty(name, defn['type'], row[defn['column']], source, identity)
                    except IndexError:
                        self._logger.critical(repr(defn))
                        self._logger.critical(repr(row))
                        retcode = 500
                        break


                    data.type_id = defn['type_id']
                    values.append(data)

                if retcode != 200:
                    break

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
                        if 'assoc_type_id' not in defn:
                            defn['assoc_type_id'], assoc_name = self.find_or_create_assoc_defn(source, defn['source'], name)
                            assoc_dao.create_mapping(defn['type_id'], prop_by_column[defn['column']].ident, defn['assoc_type_id'])

                record = SourceEntity()
                record.values = values
                entity_id = self.edit_source(record)
                self.update_associations(entity_id, [])
                self._connection.commit()

            self._cursor.close()
            self._connection.close()

            return retcode

    def edit_source(self, source_rec):

        entity_id = None
        id_prop = None

        id_properties = []
        for prop in source_rec.values:
            if isinstance(prop, BulkLoadProperty):
                if not prop.type_id:
                    prop_type = self.find_or_create_prop_defn(prop.source, prop.data_name,
                                                              prop.data_type, prop.identity, 0,
                                                              True)
                    prop.type_id = prop_type.ident

            if prop.identity:
                id_properties.append(prop)
                if self.get_prop_value(prop) is None or (prop.data_type == 'string' and prop.data_value == ''):
                    self._logger.error("No key value:" + repr(prop))
#                print (repr(prop))


        entity_id, found = self.find_entity(id_properties)

        self.save_entity(entity_id, source_rec, False)

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
            raise InvalidIdException("No identity properties for :" + source)

        res = cursor.fetchone()
        if res:
            self._logger.error(source + ''' uses a combination key and can't be retrieved by this method ''' + repr(result) + repr(res))
            cursor.close()
            connection.close()
            raise IncompleteCombinationKeyException("Cannot fetch record with only one part of a combination key")

        prop_type_id = result[0]
        prop_type = result[1]

        data_field = self.get_data_field(prop_type.decode('utf-8'))

        entity_query = '''SELECT
            HEX(e.id), ep.entity_id
            FROM
                properties p
            JOIN property_types pt
                ON pt.id = p.prop_type_id AND pt.identity = 1
            JOIN entity_properties ep ON ep.property_id = p.id
            JOIN entities e ON e.added_id = ep.entity_id
            WHERE `''' + data_field + "` = %s AND p.prop_type_id = %s"

        cursor.execute(entity_query, (source_id, prop_type_id))
        entity = cursor.fetchone()

        if not entity:
            cursor.close()
            connection.close()
            raise InvalidIdException("No record found for: {} {}".format(source, source_id))

        entity_id = entity[0]
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

        q = ("SELECT id, prop_type FROM `property_types` WHERE `source` = %s AND `prop_name` = %s")
        self._cursor.execute(q, (source, prop_name,))

        property_type_id = None
        property_type = None
        for (pti, pt) in self._cursor:
            property_type_id = pti
            property_type = pt

        query = ('''SELECT count(ep.property_id), pt.`source`, pt.prop_name, pt.prop_type, p.''' + self.get_data_field(property_type.decode('utf-8')) + ''' from entity_properties ep
            JOIN properties p ON p.id = ep.property_id
            JOIN property_types pt ON pt.id = p.prop_type_id
            WHERE `pt`.`source` = %s AND `pt`.`prop_name` = %s
            GROUP BY (ep.property_id) HAVING COUNT(ep.property_id) > %s order by prop_name, ''' +
                 self.get_data_field(property_type.decode('utf-8')))


        self._cursor.execute(query, (source, prop_name, th))

        results = []
        for (count, source, pname, ptype, pvalue) in self._cursor:
            summ = SummaryItem()
            summ.source_name = pvalue.decode("utf-8")
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
            summ.source_name = pname.decode('utf-8')
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
            summ.source_name = source.decode('utf-8')
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
