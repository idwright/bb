from backbone_server.dao.base_dao import BaseDAO
from backbone_server.dao.association_dao import AssociationDAO
from backbone_server.dao.model.property_type import PropertyType
from backbone_server.dao.model.association_type import AssociationType
from backbone_server.dao.model.server_property import ServerProperty
from backbone_server.errors.invalid_id_exception import InvalidIdException
from backbone_server.errors.no_such_type_exception import NoSuchTypeException
from backbone_server.errors.duplicate_property_exception import DuplicatePropertyException
from backbone_server.errors.invalid_data_value_exception import InvalidDataValueException
from swagger_server.models.entity import Entity
from swagger_server.models.entities import Entities
from swagger_server.models.fields import Fields
from swagger_server.models.property import Property
from swagger_server.models.relationship import Relationship
from swagger_server.models.summary_item import SummaryItem
import mysql.connector
from mysql.connector import errorcode
import uuid
import logging
import psycopg2

class EntityDAO(BaseDAO):

    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(__name__)

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

        self.save_entity(internal_id, entity, True)

        self._connection.commit()
        retval = self.get_entity_by_id(entity.entity_id, internal_id)
        self._cursor.close()
        self._connection.close()


        return retval

    def update_associations(self, internal_id, fk_keys):

        assoc_dao = AssociationDAO(self._cursor)

        fk_keys.append(internal_id)

        i = 0

        for int_id in fk_keys:
            missing_sources = assoc_dao.find_missing_association_sources(int_id)

            for missing in missing_sources:
                fk, found = self.find_or_create_entity([missing])
                if not found:
                    #print(str(missing.type_id) + "\n" + str(fk) + "\n" + repr(missing))
                    self._system_fk_data.data_value = "true"
                    self.add_entity_property(fk, self._system_fk_data)
                    self.add_entity_property(fk, missing)
                    i = i + 1
                #else:
                #    print("Found!!!!!" + str(missing.type_id) + repr(missing))

            assoc_dao.merge_implied_associations(int_id)
            assoc_dao.create_implied_associations(int_id)
            missing_sources = assoc_dao.delete_implied_associations(int_id)

        return i

    """
        :return: True if a property is modified
    """
    def save_entity(self, internal_id, entity, update_associations):

        if not internal_id:
            self._cursor.close()
            self._connection.close()
            raise InvalidIdException("Invalid id:" + entity.entity_id)

        #Initialization of this is not ideal but not a good idea to do in __init__
        self._system_fk_type = self.find_or_create_prop_defn('system', 'implied_id', 'boolean', False, 0, False)
        self._system_fk_data = ServerProperty('implied_id', 'boolean', 'false', 'system', False)
        self._system_fk_data.type_id = self._system_fk_type.ident

        self._system_fk_data.data_value = 'false'
        modified = self.add_entity_property(internal_id, self._system_fk_data)

        props = {}

        for prop in entity.values:
            if not isinstance(prop, ServerProperty):
                property_type = self.find_or_create_prop_defn(prop.source, prop.data_name,
                                                              prop.data_type, prop.identity, 0, True)
                sprop = ServerProperty(prop.data_name, prop.data_type, prop.data_value, prop.source,
                                                       prop.identity)
                prop = sprop
                prop.type_id = property_type.ident
            if prop.type_id in props:
                self._cursor.close()
                self._connection.close()
                raise DuplicatePropertyException("Duplicate properties: {} {} {} {}".format(
                    prop.source, prop.data_name,
                    prop.data_value, props[prop.type_id].data_value))
            props[prop.type_id] = prop
            if prop.data_value != '':
                modified = self.add_entity_property(internal_id, prop) or modified

        fk_keys = []
        if entity.refs:
            for assoc in entity.refs:
                assoc_type = AssociationType()
                assoc_type.assoc_name = assoc.assoc_name
                assoc_type = self.find_or_create_assoc_type(assoc_type)
                internal_source_id = self.get_internal_id(assoc.source_id)
                internal_target_id = self.get_internal_id(assoc.target_id)
                if internal_source_id == internal_id:
                    fk_keys.append(internal_target_id)
                else:
                    fk_keys.append(internal_source_id)
                self.add_assoc(internal_source_id, internal_target_id, assoc_type.ident)
                if assoc.values:
                    props = {}
                    for prop in assoc.values:
                        if isinstance(prop, ServerProperty):
                            property_type_id = prop.type_id
                        else:
                            property_type = self.find_or_create_prop_defn(prop.source, prop.data_name,
                                                                      prop.data_type, prop.identity, 0, True)
                            property_type_id = property_type.ident
                            sprop = ServerProperty(prop.data_name, prop.data_type, prop.data_value, prop.source,
                                                       prop.identity)
                            prop = sprop
                            prop.type_id = property_type.ident
                        if property_type_id in props:
                            self._cursor.close()
                            self._connection.close()
                            raise DuplicatePropertyException("Duplicate properties: {} {} {} {}".format(
                                prop.source, prop.data_name,
                                prop.data_value, props[property_type_id].data_value))
                        props[property_type_id] = prop
                        self.add_assoc_property(internal_source_id, internal_target_id, assoc_type, prop, property_type_id)

        if update_associations:
            self.update_associations(internal_id, fk_keys)

        return modified


    def find_or_create_assoc_type(self, assoc_type):

        self._cursor.execute("SELECT id, assoc_type FROM assoc_types WHERE assoc_name = %s",
                             (assoc_type.assoc_name,))

        for (ati, att) in self._cursor:
            assoc_type.ident = ati
            assoc_type.assoc_type = att

        if not assoc_type.ident:
            self._cursor.execute(BaseDAO.insert_statement("INSERT INTO assoc_types (assoc_name, assoc_type) VALUES (%s, %s)"), 
                                 (assoc_type.assoc_name, assoc_type.assoc_type))
            assoc_type.ident = BaseDAO.inserted_id(self._cursor)
#            cnx.commit()
#        cursor.close()
#        cnx.close()

        return assoc_type

    def find_or_create_prop_defn(self, source, name, data_type, identity, order, versionable):
#        cnx = self.get_connection()
#        cursor = cnx.cursor()

        self._cursor.execute("SELECT id FROM property_types WHERE source = %s AND prop_name = %s AND prop_type = %s", (source, name, data_type))

        property_type_id = None
        for (pti,) in self._cursor:
            property_type_id = pti

        if not property_type_id:
            try:
                self._cursor.execute(BaseDAO.insert_statement('''INSERT INTO property_types (source, prop_name, prop_type,
                                 prop_order, identity) VALUES (%s, %s, %s, %s, %s)'''),
                                 (source, name, data_type, order, identity))
            except mysql.connector.Error as err:
                #MySQL
                if err.errno == errorcode.ER_DUP_ENTRY:
                    raise InvalidDataValueException("Error inserting property {} {} {} {} - probably type mismatch"
                                                    .format(source, name, data_type, str(order))) from err
                else:
                    self._logger.fatal(repr(error))
            except psycopg2.IntegrityError as err:
                raise InvalidDataValueException("Error inserting property {} {} {} {} - probably type mismatch"
                                                    .format(source, name, data_type, str(order))) from err
            except:
                self._logger.exception('')
            property_type_id = BaseDAO.inserted_id(self._cursor)
            #cnx.commit()
#        cursor.close()
#        cnx.close()
        pt = PropertyType(ident=property_type_id, prop_name=name, prop_type=data_type, prop_order=order,
                          source=source, identity=identity, versionable=versionable)

        return pt

    def update_property(self, prop, property_id, old_value):
        #Need to check if there are other entities referencing the same property before updating
        count = self.count_entities_with_property_value(property_id, old_value, prop.data_field)
        #print("count:" + str(count))
        if count == 1:
            #Update property value
            #print("updating property:" + str(property_id) + repr(prop) + " type:" + str(type(prop.typed_data_value)))
            #print("updating property old_value:" + str(old_value) + " type:" + str(type(old_value)))
            update_prop = ("UPDATE properties SET " + prop.data_field + " = %s WHERE id = %s;")
            try:
                self._cursor.execute(update_prop, (prop.typed_data_value, property_id))
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_WARN_DATA_OUT_OF_RANGE:
                    raise InvalidDataValueException("Bad value for property id {} {}"
                                                    .format(property_id, str(prop.typed_data_value))) from err
            return True

        return False

    """
        adds a Property to an entity

        :param prop:
        :type prop: Property

        :rtype: None
    """
    def add_or_update_property_entity(self, entity_id, prop):

        fetch_row = ("SELECT e.added_id, p.id as property_id, " + prop.data_field + ''' FROM properties p
                     JOIN property_types AS pt ON pt.id = p.prop_type_id
                     JOIN entity_properties AS ep ON ep.property_id = p.id
                     JOIN entities AS e ON ep.entity_id = e.added_id
                     WHERE p.prop_type_id = %s AND added_id = %s''')

        self._cursor.execute(fetch_row, (prop.type_id, entity_id))
        property_id = None
        old_value = None

        #print (fetch_row % (prop.type_id, entity_id))
        prop_matched_id = None
        for (added_id, prop_id, old_v) in self._cursor:
            if prop.compare(ServerProperty.from_db_value(prop.data_type,old_v)):
                #print ("match")
                prop_matched_id = prop_id
                return prop_id, None, True, False
            else:
                if property_id:
                    self._logger.warn("Multiple values for:" + entity_id + repr(prop))
                    #print("Multiple values for:" + str(entity_id) + repr(prop))
               # print ("no match for:" + str(entity_id) + " " +
               #        str(ServerProperty.from_db_value(prop.data_type, old_v)) + " != " + str(prop.typed_data_value))
               # print ("no match for:" + str(entity_id) + " " +
               #        str(type(ServerProperty.from_db_value(prop.data_type, old_v))) + " != " +
               #        str(type(prop.typed_data_value)))
               # print (fetch_row % (prop.type_id, entity_id))
                property_id = prop_id
                if self.update_property(prop, property_id,
                                        ServerProperty.from_db_value(prop.data_type, old_v)):
                    return property_id, None, True, True

#        cursor.close()
#        cnx.close()
        return self.insert_property(prop), property_id, False, True


    """
        adds a Property to an entity

        :param prop:
        :type prop: Property

        :return: True if a change has been made
        :rtype: bool
    """
    def add_entity_property(self, entity_id, prop):

        #print("Add entity_property:" + str(entity_id) + " " + repr(prop))
        property_id, delete_old, linked, modified = self.add_or_update_property_entity(entity_id, prop)

        #print("add_entity_property:" + str(property_id) + str(create) + str(delete_old) + str(exists) + str(linked))
        if delete_old:
            old_property_id = delete_old
            #Note - do not delete the old property, intended to be used for history
            #print ("Delete reference to old property value:" + str(entity_id) + ":" + str(old_property_id))
            self._cursor.execute("DELETE FROM entity_properties WHERE entity_id = %s AND property_id = %s", (entity_id, old_property_id))
        if not linked:
            #print ("insert reference to new property value:" + str(entity_id) + ":" + str(property_id))
            self._cursor.execute("INSERT INTO entity_properties (entity_id, property_id) VALUES (%s, %s)", (entity_id, property_id))

        #if modified:
        #    print("Modified entity_property:" + str(entity_id) + " " + repr(prop))
        return modified

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
            'integer': lambda x: None if x is None or x.lower() == "null" or x == '' else int(x),
            'float': lambda x: float(x),
            'double': lambda x: float(x),
            'json': lambda x: x,
            'boolean': lambda x: 1 if x.lower() == 'true' else 0,
            'datetime': lambda x: None if x is None or x.lower() == "null" or x == '' else x,
            }.get(data_type)(data_value)

        return converted_field


    def get_db_prop_value(self, prop, db_value):

        converted_field = {
            'string': lambda x: None if x is None else BaseDAO._decode(x),
            'integer': lambda x: x,
            'float': lambda x: x,
            'double': lambda x: x,
            'json': lambda x: x,
            'boolean': lambda x: x,
            'datetime': lambda x: x,
            }.get(prop.data_type)(db_value)

        return converted_field

    def add_or_update_assoc_property(self, entity_id, fk, assoc_type, prop, property_type_id):

        fetch_row = ("SELECT p.id as property_id, " + prop.data_field + " FROM properties p JOIN assoc_properties AS ap ON ap.property_id = p.id WHERE p.prop_type_id = %s AND source_entity_id = %s AND target_entity_id = %s AND assoc_type_id = %s")

        values = (property_type_id, entity_id, fk, assoc_type.ident)
        #print(fetch_row)
        #print(repr(values))
        self._cursor.execute(fetch_row, values)
        property_id = None
        old_value = None

        for (prop_id, value) in self._cursor:
            old_val = self.get_db_prop_value(prop, value)
            if old_val == prop.typed_data_value:
                prop_matched_id = prop_id
                return prop_id, None, True
            else:
                old_value = old_val
                property_id = prop_id
                if self.update_property(prop, property_id, old_value):
                    return property_id, None, True

        return self.insert_property(prop), property_id, False


    """
        Finds if more than one entity/association references a given property - misleading name

        :param property_id: the id of an existing property which matches prop
        :type property_id: int
        :param old_value: the current value in property_id
        :return: property_id, created, multiple_values, updated, matched

        :rtype: int
    """
    def count_entities_with_property_value(self, property_id, old_value, data_field):

        count = 0
        count_query = "SELECT p.id FROM properties p LEFT JOIN entity_properties AS ep ON ep.property_id = p.id LEFT JOIN assoc_properties AS ap ON ap.property_id = p.id WHERE " + data_field + " = %s and p.id = %s LIMIT 5"

        try:

            self._cursor.execute(count_query, (old_value, property_id))

            #Neither of these work
            #count = self._cursor.rowcount
            #results = self._connection.get_rows(count)
            #count = len(results)

            for (pid,) in self._cursor:
                count = count + 1
                pass
            #print(count_query)
        except:
            count_query = count_query.replace('%s', '{}')
            self._logger.warn("count_entities_with_property_value:" + count_query.format(old_value, property_id))

        return count

    def find_property_with_value(self, prop):
        count_query = ("SELECT p.id FROM properties p JOIN property_types AS pt ON pt.id = p.prop_type_id WHERE " + prop.data_field + " = %s AND pt.source = %s AND pt.prop_name = %s AND pt.prop_type = %s")

        #print(count_query)
        #print(repr(prop))
        existing_property_id = None

        try:
            self._cursor.execute(count_query, (prop.typed_data_value, prop.source, prop.data_name, prop.data_type))

            for (prop_id,) in self._cursor:
                existing_property_id = prop_id
        except ValueError:
            self._logger.error("Failed search for:" + repr(prop))

        return existing_property_id

    """
        adds or updates a Property

        :param prop:
        :type prop: Property
        :param data_field: which data field the value is held in
        :param property_id: the id of an existing property which matches prop
        :type property_id: int
        :param old_value: the current value in property_id
        :return: property_id, created, multiple_values, updated, matched

        :rtype: int
    """
    def insert_property(self, prop):

        #print("insert_property:" + str(data_field) + " property_id:" + str(property_id))
        #print("insert_property old_value:" + str(old_value) + " type:" + str(type(old_value)))
        self._logger.debug("insert_property:" + repr(prop))

        existing_property_id = self.find_property_with_value(prop)

        if existing_property_id:
            #print("update_property: existing property found")
            return existing_property_id

        #print ("insert_property: inserting")
        insert_statement = BaseDAO.insert_statement("INSERT INTO properties (prop_type_id, " + prop.data_field + ") VALUES (%s, %s)")

        #print(insert_statement)
        #print (repr(prop))
        try:
            self._cursor.execute(insert_statement, (prop.type_id, prop.typed_data_value))
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_WARN_DATA_OUT_OF_RANGE:
                raise InvalidDataValueException("Bad value for property {} {}".format(prop.type_id,
                                                                                      str(prop.typed_data_value))) from err
        new_property_id = BaseDAO.inserted_id(self._cursor)
        #print ("Added property id:" + str(new_property_id) + repr(prop))

        return new_property_id

    def add_assoc_property(self, entity_id, fk, assoc_type, prop, property_type_id):

        property_id, delete_old, linked = self.add_or_update_assoc_property(entity_id, fk, assoc_type, prop, property_type_id)

        if delete_old:
            old_property_id = delete_old
            #Note - do not delete the old property, intended to be used for history
            #            print ("Delete reference to old property value:" +
            #            str(entity_id) + ":" + str(old_property_id))
            self._cursor.execute('''DELETE FROM entity_properties WHERE source_entity_id = %s AND
                                 target_entity_id = %s AND assoc_type_id = %s AND property_id = %s''',
                                 (entity_id, fk, assoc_type.ident, old_property_id))

        if not linked:
#            cnx = self.get_connection()
#            cursor = cnx.cursor()
            query = ("INSERT INTO assoc_properties (source_entity_id, target_entity_id, assoc_type_id, property_id) VALUES (%s, %s, %s, %s)")

            self._cursor.execute(query, (entity_id, fk, assoc_type.ident, property_id))

#            cnx.commit()
#            cursor.close()
#            cnx.close()


    def find_entity_by_fk(self, prop):

        if self._postgres:
            sel = "SELECT e.id"
        else:
            sel = "SELECT HEX(e.id)"
        fetch_row = (sel + ''',e.added_id FROM assoc_mappings am
                        JOIN property_types spt ON spt.id = am.source_prop_type_id
                         JOIN property_types tpt ON tpt.id = am.source_prop_type_id
                         JOIN assoc_types atp ON atp.id = am.assoc_type_id
                         JOIN properties p ON p.prop_type_id = am.source_prop_type_id
                         JOIN entity_properties ep ON ep.property_id = p.id
                         JOIN entities e ON e.added_id = ep.entity_id
                         WHERE am.target_prop_type_id=%s AND p.''' +
                     self.get_data_field(prop.data_type) + ''' = %s ''')

        #print(fetch_row % (prop.type_id, prop.data_value))
        self._cursor.execute(fetch_row, (prop.type_id, prop.data_value))

        property_details = []
        for (entity_id, added_id) in self._cursor:
            property_details.append({'entity_id': str(entity_id), 'added_id': added_id})

        found = False
        parent_entity_id = None

        if len(property_details) == 1:
#            print ("Found entity:" + repr(property_details))
            parent_entity_id = property_details[0]['added_id']
            found = True
        elif len(property_details) > 1:
            self._logger.critical("Duplicate entities:" + repr(prop))

        return parent_entity_id, found


    def find_entity_by_properties(self, properties):

        if self._postgres:
            sel = "SELECT e.id"
        else:
            sel = "SELECT HEX(e.id)"
        fetch_row = (sel + ''', e.added_id
                    FROM
                        properties p
                        JOIN property_types pt ON pt.id = p.prop_type_id
                        JOIN entity_properties ep ON ep.property_id = p.id
                        JOIN entities e ON e.added_id = ep.entity_id
                    WHERE ''')

        filters = []
        values = []
        for prop in properties:
            pfilter = 'prop_name = %s AND source = %s'
            values.append(prop.data_name)
            values.append(prop.source)
            if prop.data_value:
                pfilter = pfilter + " AND " + self.get_data_field(prop.data_type) +" = %s"
                values.append(prop.data_value)
            filters.append(pfilter)

        fetch_row = fetch_row + ' AND '.join(filters)

        if not filters:
            raise InvalidIdException("No properties to search")

        #print(fetch_row % filters)

        self._cursor.execute(fetch_row, values)

        property_details = []
        for (entity_id, added_id) in self._cursor:
            property_details.append({'entity_id': str(entity_id), 'added_id': added_id})
#        print((prop_name, source, prop_value))
#        print (property_details)
#        cursor.close()
#        cnx.close()

        return property_details

    def find_entity(self, id_properties):

        found = False
        parent_entity_id = None

        property_details = self.find_entity_by_properties(id_properties)

        #print(property_details)
        if len(property_details) == 1:
#            print ("Found entity:" + repr(property_details))
            parent_entity_id = property_details[0]['added_id']
            found = True
        elif len(property_details) > 1:
            self._logger.critical("Duplicate entities:" + repr(id_properties))

        return parent_entity_id, found

    def create_entity(self):
        parent_entity_id = None
        if self._postgres:
            query = ("INSERT INTO entities (id) VALUES (%s) RETURNING added_id")
            uuid_val = uuid.uuid4()
            args = (uuid_val,)
            self._cursor.execute(query, args)
            parent_entity_id = self._cursor.fetchone()[0]
        else:
            query = ("INSERT INTO entities (id) VALUES ((ordered_uuid(uuid())))")
            args = ()

            self._cursor.execute(query, args)
            parent_entity_id = self._cursor.lastrowid

        return parent_entity_id

    def find_or_create_entity(self, id_properties):

        parent_entity_id, found = self.find_entity(id_properties)

        if not found:
            parent_entity_id = self.create_entity()

        return parent_entity_id, found

    def add_assoc(self, entity_id, fk, assoc_type_id):
#        cnx = self.get_connection()
#        cursor = cnx.cursor()
        query = ("INSERT INTO entity_assoc (source_entity_id, target_entity_id, assoc_type_id) VALUES (%s, %s, %s)")
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

        if self._postgres:
            added_id_query = 'SELECT added_id FROM entities WHERE id = (%s);'
            entity_id = uuid.UUID(entity_id)
        else:
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
        props_query = 'SELECT source, prop_name, prop_type, value, identity FROM property_values WHERE added_id = %s'

        self._cursor.execute(props_query, (added_id,))

        properties = []
        for (source, prop_name, prop_type, prop_value, identity) in self._cursor:
            data = Property()
            data.data_type = BaseDAO._decode(prop_type)
            data.data_name = BaseDAO._decode(prop_name)
            data.identity = bool(identity)
            data.source = BaseDAO._decode(source)
            if isinstance(prop_value, memoryview):
                prop_value = bytes(prop_value).decode('utf-8')
            if prop_value is None:
                data.data_value = ''
            else:
                #Conversion to string is done in the property_values view
                data.data_value = prop_value
            properties.append(data)

        entity.values = properties
        assocs_query = '''SELECT source_uuid, source_id, target_uuid, target_id, assoc_name, assoc_type_id FROM associations
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
            fetch_row = '''select source, prop_name, prop_type, value, identity from association_property_values
                            WHERE source_id = %s AND target_id = %s AND assoc_type_id = %s'''
            self._cursor.execute(fetch_row, (sad, tad, ati))
            values = []
            for (source, prop_name, prop_type, prop_value, identity) in self._cursor:
                data = Property()
                data.data_type = BaseDAO._decode(prop_type)
                data.data_name = BaseDAO._decode(prop_name)
                data.identity = bool(identity)
                data.source = BaseDAO._decode(source)
                if isinstance(prop_value, memoryview):
                    prop_value = bytes(prop_value).decode('utf-8')
                if prop_value is None:
                    data.data_value = ''
                else:
                    data.data_value = prop_value
                values.append(data)

            suuid = str(ad[0])
            tuuid = str(ad[2])
#            if self._postgres:
#                suuid = uuid.UUID(suuid)
#                tuuid = uuid.UUID(tuuid)
            data = Relationship(tuuid, suuid, assoc_name, values)
            refs.append(data)


        entity.refs = refs
        #print ("Fetched entity:" + str(added_id))
        return entity

    def get_properties_by_name(self, source, prop_name):

        self._cursor.execute("SELECT id, prop_type, source FROM property_types WHERE prop_name = %s", (prop_name,))
        props = []
        for (pti, pt, src) in self._cursor:
            prop = ServerProperty()
            prop.type_id = pti
            prop.data_type = BaseDAO._decode(pt)
            prop.data_name = prop_name
            prop.source = BaseDAO._decode(src)
            if source is None or prop.source == source:
                props.append(prop)

        if len(props) == 0:
            raise NoSuchTypeException("No such type:" + prop_name)

        return props

    def fetch_entities_by_property(self, source, prop_name, prop_value, start, count, orderby):

        self._connection = self.get_connection()
        self._cursor = self._connection.cursor()


        result = Entities()
        result.count = 0
        entities = []

        props = self.get_properties_by_name(source, prop_name)

        if self._postgres:
            sel = "SELECT e.id"
        else:
            sel = "SELECT HEX(e.id)"
        for prop in props:
            prop.data_value = prop_value
            props_query = sel + ''', e.added_id
                FROM
                    properties p
                JOIN entity_properties ep ON ep.property_id = p.id
                JOIN entities e ON e.added_id = ep.entity_id'''

            where_clause = ' WHERE prop_type_id = %s '
            if prop_value == "*":
                where_clause = where_clause + ' AND ' + prop.data_field + ' IS NOT NULL'
                query_args = (prop.type_id, )
            else:
                where_clause = where_clause + ' AND ' + prop.data_field + ' = %s'
                query_args = (prop.type_id, prop.typed_data_value,)

            props_query = props_query + where_clause

            #print(str(start) + str(count))
            if not (start is None and count is None):
                props_query = props_query + ' ORDER BY e.added_id LIMIT ' + str(count) + " OFFSET " + str(start)
                #print(props_query % query_args))
            if count is None or int(count) == 0 or len(entities) < int(count):
                try:
                    self._cursor.execute(props_query, query_args)

                    ents = []
                    for (ent_id, added_id,) in self._cursor:
                        ents.append({'ent_id': str(ent_id), 'added_id': added_id})

                    for ent in ents:
                        entities.append(self.get_entity_by_id(ent["ent_id"], ent["added_id"]))
                except ValueError:
                    self._logger.warn("Mismatch type when searching: {} {} {}"
                                      .format(prop_name, prop_value, repr(prop)))

            #Note that there is never a limit on the count, which is why it's a separate query
            count_query = '''SELECT
                    COUNT(e.added_id)
                    FROM
                        properties p
                    JOIN entity_properties ep ON ep.property_id = p.id
                    JOIN entities e ON e.added_id = ep.entity_id ''' + where_clause

            try:
                #print(count_query % query_args)
                self._cursor.execute(count_query, query_args)

                result.count = result.count + self._cursor.fetchone()[0]
            except ValueError:
                self._logger.warn("Mismatch type when searching: {}"
                                  .format(repr(prop)))

        self._cursor.close()
        self._connection.close()

        result.entities = entities
        return result

    def fetch_fields_by_property(self, sources, prop_name, prop_value, include_filter):

        self._connection = self.get_connection()
        self._cursor = self._connection.cursor()


        result = Fields()
        entities = []
        cols = []
        source_list = [None]
        if sources:
            source_list = sources.split(",")

        if include_filter == "all":
            pass
        else:
            for source in source_list:
                props = self.get_properties_by_name(source, prop_name)

                for prop in props:
                    prop.data_value = prop_value

                    new_columns = self.find_columns(prop)
                    old_set = set(cols)
                    cols = cols + [x for x in new_columns if x not in old_set]

        self._cursor.close()
        self._connection.close()

        result.fields = cols

        return result

    def find_columns(self, prop):

        where_clause = ' WHERE prop_type_id = %s AND source = %s '
        query_args = ()

        if prop.data_value == '*':
            where_clause = where_clause + ' AND ' + prop.data_field + ' IS NOT NULL '
            query_args = (prop.type_id, prop.source)
        else:
            where_clause = where_clause + ' AND ' + prop.data_field + ' = %s '
            query_args = (prop.type_id, prop.source, prop.typed_data_value)

        columns_query = '''SELECT
    pt.source, pt.prop_name, pt.prop_type, pt.identity
FROM
    properties p
        JOIN
    property_types pt ON p.prop_type_id = pt.id
WHERE
    p.id IN (SELECT DISTINCT
            ep.property_id
        FROM
            entity_properties ep
        WHERE
            ep.entity_id IN (SELECT DISTINCT
                    ep.entity_id
                FROM
                    properties p
                        JOIN
                    entity_properties ep ON ep.property_id = p.id
                        JOIN
                    property_types pt ON p.prop_type_id = pt.id ''' + where_clause + '''))
GROUP BY pt.id
ORDER BY pt.source , pt.prop_order, pt.prop_name;'''

        #print(columns_query % query_args)
        self._cursor.execute(columns_query, query_args)
        columns = []
        for (source, prop_name, prop_type, identity) in self._cursor:
            sprop = ServerProperty()
            sprop.data_name = BaseDAO._decode(prop_name)
            sprop.source = BaseDAO._decode(source)
            sprop.prop_type = BaseDAO._decode(prop_type)
            sprop.identity = ServerProperty.from_db_value('boolean', identity)
            columns.append(sprop)

        return columns

    def get_properties(self, source):

        self._connection = self.get_connection()
        self._cursor = self._connection.cursor()

        pfilter = ''
        params = ()
        if source:
            pfilter = ' WHERE pt.source = %s '
            params = (source,)
            query = '''SELECT COUNT(pt.prop_name), pt.prop_name, pt.source from property_types pt
            JOIN properties p ON p.prop_type_id = pt.id''' + pfilter + '''
                    GROUP BY pt.source, pt.prop_name;'''


            #print(query % params)
            self._cursor.execute(query, params)

            results = []
            for (count, pname, psource) in self._cursor:
                summ = SummaryItem()
                summ.source_name = BaseDAO._decode(psource)
                summ.prop_name = BaseDAO._decode(pname)
                summ.num_items = count
                results.append(summ)
        else:
            query = '''SELECT COUNT(pt.prop_name), pt.prop_name from property_types pt
            JOIN properties p ON p.prop_type_id = pt.id
                    GROUP BY pt.prop_name ORDER BY CONVERT (pt.prop_name USING utf8);'''


            #print(query)
            self._cursor.execute(query)

            results = []
            for (count, pname) in self._cursor:
                summ = SummaryItem()
                summ.prop_name = BaseDAO._decode(pname)
                summ.num_items = count
                results.append(summ)

        self._connection.commit()
        self._cursor.close()
        self._connection.close()

        return results

    def get_summary_by_property(self, source, prop_name, threshold):

        th = 0
        if threshold:
            th = threshold

        self._connection = self.get_connection()
        self._cursor = self._connection.cursor()

        props = self.get_properties_by_name(source, prop_name)

        prop = props[0]

        if source:
            pfilter = ' pt.source = %s AND '
            qargs = (source, prop_name, th)
        else:
            pfilter = ''
            qargs = (prop_name, th)

        query = ('''SELECT count(ep.property_id), pt.prop_name, p.''' +
                 prop.data_field + ''' from entity_properties ep
            JOIN properties p ON p.id = ep.property_id
            JOIN property_types pt ON pt.id = p.prop_type_id
            WHERE ''' + pfilter + ''' pt.prop_name = %s
            GROUP BY (''' + prop.data_field + ''') HAVING COUNT(''' + prop.data_field + ''') > %s
                 order by CONVERT (prop_name USING utf8), ''' +
                 prop.data_field)


        #print(query % qargs)
        self._cursor.execute(query, qargs)

        results = []
        for (count, pname, pvalue) in self._cursor:
            #print(repr(prop), pvalue)
            summ = SummaryItem()
            summ.source_name = str(ServerProperty.from_db_value(prop.data_type, pvalue))
            summ.num_items = count
            results.append(summ)

        self._connection.commit()
        self._cursor.close()
        self._connection.close()

        return results

#if __name__ == '__main__':
#    sd = source_dao()
#    data_def = json.loads('{ "refs": { "oxf_code": { "column": 1, "type": "string", "source": "lims" }}, "values":{ "id": { "column": 24, "type": "integer", "id": true }, "sample_type": { "column": 6, "type": "string" } } }')
#    sd.load_data('test', data_def)
#
#    print(repr(sd.fetch_entity_by_source('test',1)))
