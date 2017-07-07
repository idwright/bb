from backbone_server.dao.base_dao import BaseDAO
from backbone_server.dao.association_dao import AssociationDAO
from backbone_server.dao.model.property_type import PropertyType
from backbone_server.dao.model.association_type import AssociationType
from backbone_server.dao.model.server_property import ServerProperty
from backbone_server.errors.invalid_id_exception import InvalidIdException
from backbone_server.errors.no_such_type_exception import NoSuchTypeException
from backbone_server.errors.duplicate_property_exception import DuplicatePropertyException
from swagger_server.models.entity import Entity
from swagger_server.models.entities import Entities
from swagger_server.models.fields import Fields
from swagger_server.models.property import Property
from swagger_server.models.relationship import Relationship
from swagger_server.models.summary_item import SummaryItem
import mysql.connector
from mysql.connector import errorcode

class EntityDAO(BaseDAO):

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
                fk, found = self.find_entity([missing])
                if not found:
                    #print(str(missing.type_id) + "\n" + str(fk) + "\n" + repr(missing))
                    self._system_fk_data.data_value = "true"
                    self.add_entity_property(fk, self._system_fk_data, self._system_fk_type_id)
                    self.add_entity_property(fk, missing, missing.type_id)
                    i = i + 1
                #else:
                #    print("Found!!!!!" + str(missing.type_id) + repr(missing))

            assoc_dao.merge_implied_associations(int_id)
            assoc_dao.create_implied_associations(int_id)
            missing_sources = assoc_dao.delete_implied_associations(int_id)

        return i

    def save_entity(self, internal_id, entity, update_associations):

        if not internal_id:
            self._cursor.close()
            self._connection.close()
            raise InvalidIdException("Invalid id:" + entity.entity_id)

        #Initialization of this is not ideal but not a good idea to do in __init__
        self._system_fk_type = self.find_or_create_prop_defn('system', 'implied_id', 'boolean', False, 0, False)
        self._system_fk_type_id = self._system_fk_type.ident
        self._system_fk_data = ServerProperty('implied_id', 'boolean', 'false', 'system', False)
        self._system_fk_data.type_id = self._system_fk_type_id

        self._system_fk_data.data_value = 'false'
        self.add_entity_property(internal_id, self._system_fk_data, self._system_fk_type_id)

        props = {}
        for prop in entity.values:
            property_type_id = None
            if isinstance(prop, ServerProperty):
                property_type_id = prop.type_id
            else:
                property_type = self.find_or_create_prop_defn(prop.source, prop.data_name,
                                                              prop.data_type, prop.identity, 0, True)
                property_type_id = property_type.ident
            if property_type_id in props:
                self._cursor.close()
                self._connection.close()
                raise DuplicatePropertyException("Duplicate properties: {} {} {} {}".format(
                    prop.source, prop.data_name,
                    prop.data_value, props[property_type_id].data_value))
            props[property_type_id] = prop
            self.add_entity_property(internal_id, prop, property_type_id)

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
                        property_type = self.find_or_create_prop_defn(prop.source, prop.data_name,
                                                                      prop.data_type,
                                                                      prop.identity, 0, True)
                        property_type_id = property_type.ident
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



    def find_or_create_assoc_type(self, assoc_type):

        self._cursor.execute("SELECT id, assoc_type FROM `assoc_types` WHERE `assoc_name` = %s",
                             (assoc_type.assoc_name,))

        for (ati, att) in self._cursor:
            assoc_type.ident = ati
            assoc_type.assoc_type = att

        if not assoc_type.ident:
            self._cursor.execute("INSERT INTO `assoc_types` (`assoc_name`, `assoc_type`) VALUES (%s, %s)", 
                                 (assoc_type.assoc_name, assoc_type.assoc_type))
            assoc_type.ident = self._cursor.lastrowid
#            cnx.commit()
#        cursor.close()
#        cnx.close()

        return assoc_type

    def find_or_create_prop_defn(self, source, name, data_type, identity, order, versionable):
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
        pt = PropertyType(ident=property_type_id, prop_name=name, prop_type=data_type, prop_order=order,
                          source=source, identity=identity, versionable=versionable)

        return pt

    def update_property(self, prop, property_id, old_value, data_field):
        #Need to check if there are other entities referencing the same property before updating
        count = self.count_entities_with_property_value(property_id, old_value, data_field)
        #print("count:" + str(count))
        if count == 1:
            #Update property value
            #print("updating property:" + str(property_id) + repr(prop) + " type:" + str(type(self.get_prop_value(prop))))
            #print("updating property old_value:" + str(old_value) + " type:" + str(type(old_value)))
            update_prop = ("UPDATE properties SET `" + data_field + "` = %s WHERE id = %s;")
            self._cursor.execute(update_prop, (self.get_prop_value(prop), property_id))
            return True

        return False

    """
        adds a Property to an entity

        :param prop:
        :type prop: Property

        :rtype: None
    """
    def add_or_update_property_entity(self, entity_id, prop, property_type_id):

        data_field = self.get_data_field(prop.data_type)

        fetch_row = ("SELECT HEX(e.id),e.added_id, p.id as property_id, " + data_field + ''' FROM `properties` p
                     JOIN `property_types` AS pt ON pt.id = p.prop_type_id
                     JOIN `entity_properties` AS ep ON ep.property_id = p.id
                     JOIN `entities` AS e ON ep.entity_id = e.added_id
                     WHERE `p`.`prop_type_id` = %s AND `added_id` = %s''')

        self._cursor.execute(fetch_row, (property_type_id, entity_id))
        property_id = None
        old_value = None

        #print (fetch_row)
        #print ((prop.data_name, prop.source, entity_id))
        prop_matched_id = None
        for (ent_id, added_id, prop_id, old_v) in self._cursor:
            old_val = self.get_db_prop_value(prop, old_v)
            #print ("comparing: " + str(old_val) + " vs " + str(self.get_prop_value(prop)))
            #print ("comparing types: " + str(type(old_val)) + " vs " + str(type(self.get_prop_value(prop))))
            if old_val == self.get_prop_value(prop):
                #print ("match")
                prop_matched_id = prop_id
                return prop_id, None, True
            else:
                if property_id:
                    self._logger.warn("Multiple values for:" + entity_id + repr(prop))
                old_value = old_val
                property_id = prop_id
                if self.update_property(prop, property_id, old_value, data_field):
                    return property_id, None, True

#        cursor.close()
#        cnx.close()
        return self.insert_property(prop, property_type_id, data_field), property_id, False


    """
        adds a Property to an entity

        :param prop:
        :type prop: Property

        :rtype: None
    """
    def add_entity_property(self, entity_id, prop, property_type_id):
        #print("Add entity_property:" + str(entity_id) + " " + repr(prop))
        property_id, delete_old, linked = self.add_or_update_property_entity(entity_id, prop, property_type_id)

        #print("add_entity_property:" + str(property_id) + str(create) + str(delete_old) + str(exists) + str(linked))
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
            'integer': lambda x: None if x is None or x.lower() == "null" or x == '' else int(x),
            'float': lambda x: float(x),
            'double': lambda x: float(x),
            'json': lambda x: x,
            'boolean': lambda x: 1 if x.lower() == 'true' else 0,
            'datetime': lambda x: None if x is None or x.lower() == "null" or x == '' else x,
            }.get(data_type)(data_value)

        return converted_field

    def get_prop_value(self, prop):

        return self.get_data_value(prop.data_type, prop.data_value)

    def get_db_prop_value(self, prop, db_value):

        converted_field = {
            'string': lambda x: x.decode('utf-8'),
            'integer': lambda x: x,
            'float': lambda x: x,
            'double': lambda x: x,
            'json': lambda x: x,
            'boolean': lambda x: x,
            'datetime': lambda x: x,
            }.get(prop.data_type)(db_value)

        return converted_field

    def add_or_update_assoc_property(self, entity_id, fk, assoc_type, prop, property_type_id):

        data_field = self.get_data_field(prop.data_type)

        fetch_row = ("SELECT p.id as property_id, " + data_field + " FROM `properties` p JOIN `assoc_properties` AS ap ON ap.property_id = p.id WHERE `p`.`prop_type_id` = %s AND `source_entity_id` = %s AND `target_entity_id` = %s AND `assoc_type_id` = %s")

        values = (property_type_id, entity_id, fk, assoc_type.ident)
        #print(fetch_row)
        #print(repr(values))
        self._cursor.execute(fetch_row, values)
        property_id = None
        old_value = None

        for (prop_id, value) in self._cursor:
            old_val = self.get_db_prop_value(prop, value)
            if old_val == self.get_prop_value(prop):
                prop_matched_id = prop_id
                return prop_id, None, True
            else:
                old_value = old_val
                property_id = prop_id
                if self.update_property(prop, property_id, old_value, data_field):
                    return property_id, None, True

        return self.insert_property(prop, property_type_id, data_field), property_id, False


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
        count_query = "SELECT p.id FROM `properties` p LEFT JOIN `entity_properties` AS ep ON ep.property_id = p.id LEFT JOIN `assoc_properties` AS ap ON ap.property_id = p.id WHERE `" + data_field + "` = %s and p.id = %s LIMIT 5"

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

    def find_property_with_value(self, prop, data_field):
        count_query = ("SELECT p.id FROM `properties` p JOIN `property_types` AS pt ON pt.id = p.prop_type_id WHERE `" + data_field + "` = %s AND `pt`.`source` = %s AND `pt`.`prop_name` = %s AND `pt`.`prop_type` = %s")

        #print(count_query)
        #print(repr(prop))
        existing_property_id = None

        try:
            self._cursor.execute(count_query, (self.get_prop_value(prop), prop.source, prop.data_name, prop.data_type))

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
    def insert_property(self, prop, property_type_id, data_field):

        #print("insert_property:" + str(data_field) + " property_id:" + str(property_id))
        #print("insert_property old_value:" + str(old_value) + " type:" + str(type(old_value)))
        self._logger.debug("insert_property:" + repr(prop))

        existing_property_id = self.find_property_with_value(prop, data_field)

        if existing_property_id:
            #print("update_property: existing property found")
            return existing_property_id

        #print ("insert_property: inserting")
        insert_statement = ("INSERT INTO properties (`prop_type_id`, `" + data_field + "`) VALUES (%s, %s);")

        #print(insert_statement)
        #print (repr(prop))
        self._cursor.execute(insert_statement, (property_type_id, self.get_prop_value(prop)))
        new_property_id = self._cursor.lastrowid
        #print ("Added property id:" + str(new_property_id) + repr(prop))

        return new_property_id

    def add_assoc_property(self, entity_id, fk, assoc_type, prop, property_type_id):

        property_id, delete_old, linked = self.add_or_update_assoc_property(entity_id, fk, assoc_type, prop, property_type_id)

        if delete_old:
            old_property_id = delete_old
            #Note - do not delete the old property, intended to be used for history
            #            print ("Delete reference to old property value:" +
            #            str(entity_id) + ":" + str(old_property_id))
            self._cursor.execute('''DELETE FROM `entity_properties` WHERE `source_entity_id` = %s AND
                                 target_entity_id = %s AND assoc_type_id = %s AND `property_id` = %s''',
                                 (entity_id, fk, assoc_type.ident, old_property_id))

        if not linked:
#            cnx = self.get_connection()
#            cursor = cnx.cursor()
            query = ("INSERT INTO `assoc_properties` (`source_entity_id`, `target_entity_id`, `assoc_type_id`, `property_id`) VALUES (%s, %s, %s, %s)")

            self._cursor.execute(query, (entity_id, fk, assoc_type.ident, property_id))

#            cnx.commit()
#            cursor.close()
#            cnx.close()


    def find_entity_by_properties(self, properties):

        fetch_row = ('''SELECT
                        HEX(e.id), e.added_id
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
            property_details.append({'entity_id': entity_id, 'added_id': added_id})
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
            self._logger.critical("Duplicate entities:" + repr(id_properties))
        else:
#            cnx = self.get_connection()
#            cursor = cnx.cursor()
            query = ("INSERT INTO `entities` (`id`) VALUES (ordered_uuid(uuid()))")
            args = ()
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
        for (source, prop_name, prop_type, prop_value, identity) in self._cursor:
            data = Property()
            data.data_type = prop_type.decode('utf-8')
            data.data_name = prop_name.decode('utf-8')
            data.identity = bool(identity)
            data.source = source.decode('utf-8')
            if prop_value is None:
                data.data_value = ''
            else:
                #Conversion to string is done in the property_values view
                data.data_value = prop_value
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
            fetch_row = '''select `source`, `prop_name`, `prop_type`, `value`, `identity` from association_property_values
                            WHERE `source_id` = %s AND `target_id` = %s AND `assoc_type_id` = %s'''
            self._cursor.execute(fetch_row, (sad, tad, ati))
            values = []
            for (source, prop_name, prop_type, prop_value, identity) in self._cursor:
                data = Property()
                data.data_type = prop_type.decode('utf-8')
                data.data_name = prop_name.decode('utf-8')
                data.identity = bool(identity)
                data.source = source.decode('utf-8')
                if prop_value is None:
                    data.data_value = ''
                else:
                    data.data_value = prop_value
                values.append(data)

            data = Relationship(ad[2], ad[0], assoc_name, values)
            refs.append(data)


        entity.refs = refs
        #print ("Fetched entity:" + str(added_id))
        return entity

    def get_properties_by_name(self, source, prop_name):

        self._cursor.execute("SELECT id, prop_type, source FROM `property_types` WHERE `prop_name` = %s", (prop_name,))
        props = []
        for (pti, pt, src) in self._cursor:
            prop = ServerProperty()
            prop.type_id = pti
            prop.data_type = pt.decode('utf-8')
            prop.data_name = prop_name
            prop.source = src.decode('utf-8')
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

        for prop in props:
            prop.data_value = prop_value
            props_query = '''SELECT
                HEX(e.id), e.added_id
                FROM
                    properties p
                JOIN entity_properties ep ON ep.property_id = p.id
                JOIN entities e ON e.added_id = ep.entity_id
                WHERE prop_type_id = %s AND ''' + prop.data_field + ' = %s'

            #print(str(start) + str(count))
            if not (start is None and count is None):
                props_query = props_query + ' ORDER BY e.added_id LIMIT ' + str(count) + " OFFSET " + str(start)
            #print(props_query % (prop.type_id, prop.typed_data_value,))
            if count is None or int(count) == 0 or len(entities) < int(count):
                try:
                    self._cursor.execute(props_query, (prop.type_id, prop.typed_data_value,))

                    ents = []
                    for (ent_id, added_id,) in self._cursor:
                        ents.append({'ent_id': ent_id, 'added_id': added_id})

                    for ent in ents:
                        entities.append(self.get_entity_by_id(ent["ent_id"], ent["added_id"]))
                except ValueError:
                    self._logger.warn("Mismatch type when searching: {} {} {}"
                                      .format(prop_name, prop_value, repr(prop)))

            count_query = '''SELECT
                    COUNT(e.added_id)
                    FROM
                        properties p
                    JOIN entity_properties ep ON ep.property_id = p.id
                    JOIN entities e ON e.added_id = ep.entity_id
                    WHERE prop_type_id = %s AND ''' + prop.data_field + ' = %s'

            try:
                #print(props_query)
                #print("{} {}".format(repr(prop), repr(query_value)))
                self._cursor.execute(count_query, (prop.type_id, prop.typed_data_value,))

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

        columns_query = '''SELECT 
    pt.`source`, pt.prop_name, pt.prop_type, pt.identity
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
            ep.entity_id IN (SELECT
                    e.added_id
                FROM
                    properties p
                        JOIN
                    entity_properties ep ON ep.property_id = p.id
                        JOIN
                    entities e ON e.added_id = ep.entity_id
                WHERE
    prop_type_id = %s AND ''' + prop.data_field + ''' = %s
))
GROUP BY pt.id
ORDER BY pt.`source` , pt.prop_name;'''

        #print(columns_query % (prop.type_id, prop.typed_data_value))
        self._cursor.execute(columns_query, (prop.type_id, prop.typed_data_value))
        columns = []
        for (source, prop_name, prop_type, identity) in self._cursor:
            sprop = ServerProperty()
            sprop.data_name = prop_name.decode('utf-8')
            sprop.source = source.decode('utf-8')
            sprop.prop_type = prop_type.decode('utf-8')
            sprop.identity = sprop.from_db_value('boolean', identity)
            columns.append(sprop)

        return columns

    def get_properties(self, source):

        self._connection = self.get_connection()
        self._cursor = self._connection.cursor()

        pfilter = ''
        params = ()
        if source:
            pfilter = ' WHERE `pt`.source = %s '
            params = (source,)
            query = '''SELECT COUNT(pt.prop_name), pt.prop_name, pt.source from property_types pt
            JOIN properties p ON p.prop_type_id = pt.id''' + pfilter + '''
                    GROUP BY pt.source, pt.prop_name;'''


            #print(query % params)
            self._cursor.execute(query, params)

            results = []
            for (count, pname, psource) in self._cursor:
                summ = SummaryItem()
                summ.source_name = psource.decode('utf-8')
                summ.prop_name = pname.decode('utf-8')
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
                summ.prop_name = pname.decode('utf-8')
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
            pfilter = ' `pt`.`source` = %s AND '
            qargs = (source, prop_name, th)
        else:
            pfilter = ''
            qargs = (prop_name, th)

        query = ('''SELECT count(ep.property_id), pt.prop_name, p.''' +
                 prop.data_field + ''' from entity_properties ep
            JOIN properties p ON p.id = ep.property_id
            JOIN property_types pt ON pt.id = p.prop_type_id
            WHERE ''' + pfilter + ''' `pt`.`prop_name` = %s
            GROUP BY (''' + prop.data_field + ''') HAVING COUNT(''' + prop.data_field + ''') > %s
                 order by CONVERT (prop_name USING utf8), ''' +
                 prop.data_field)


        #print(query % qargs)
        self._cursor.execute(query, qargs)

        results = []
        for (count, pname, pvalue) in self._cursor:
            #print(repr(prop), pvalue)
            summ = SummaryItem()
            summ.source_name = str(prop.from_db_value(prop.data_type, pvalue))
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
