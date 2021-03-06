from decimal import *
import time
import datetime
from swagger_server.util import deserialize_model
from swagger_server.models.property import Property
from backbone_server.errors.invalid_data_value_exception import InvalidDataValueException
from backbone_server.dao.base_dao import BaseDAO

class ServerProperty(Property):


    def __init__(self, data_name: str=None, data_type: str='string', data_value: str=None, source:
              str=None, identity: bool=False):
        Property.__init__(self, data_name=data_name, data_type=data_type,
                          data_value=data_value, source=source, identity=identity)

        self.swagger_types['type_id'] = int
        self.attribute_map['type_id'] = 'type_id'
        self._type_id = None

    @classmethod
    def from_dict(self, dikt) -> 'ServerProperty':
        """
        Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ServerProperty of this Property.
        :rtype: ServerProperty
        """
        return deserialize_model(dikt, self)

    def __hash__(self):
        return hash(repr(self.to_dict()))

    @classmethod
    def get_default_date_format(klass):
        return klass.default_date_format

    @property
    def default_date_format(self) -> str:
        return '%Y-%m-%d %H:%M:%S'

    @property
    def type_id(self) -> int:
        """
        Gets the identity of this Property.
        If this an identity column

        :return: The identity of this Property.
        :rtype: bool
        """
        return self._type_id

    @type_id.setter
    def type_id(self, type_id: int):
        """
        Sets the identity of this Property.
        If this an identity column

        :param identity: The identity of this Property.
        :type identity: bool
        """

        self._type_id = type_id


    @property
    def data_field(self):
        data_field = {
            'string': "string_value",
            'integer': "long_value",
            'float': "float_value",
            'double': "double_value",
            'json': "json_value",
            'boolean': "boolean_value",
            'datetime': "datetime_value",
        }.get(self._data_type, 'string_value')

        return data_field

    @staticmethod
    def float_value(x):
        getcontext().prec = 6

        return Decimal(x)

    @staticmethod
    def double_value(x):
        getcontext().prec = 12

        return Decimal(x)

    @property
    def typed_data_value(self):

        try:
            converted_field = {
                'string': lambda x: x,
                'integer': lambda x: None if x is None or x.lower() == "null" or x == '' or x.lower() == 'na' else int(x),
                'float': lambda x: ServerProperty.float_value(x),
                'double': lambda x: ServerProperty.double_value(x),
                'json': lambda x: x,
                'boolean': lambda x: True if x.lower() == 'true' or x.lower() == 'yes' else False,
                'datetime': lambda x: x if isinstance(x, datetime.datetime) else 
                    datetime.datetime(*(time.strptime(x, self.default_date_format))[:6])
                ,
                }.get(self._data_type)(self._data_value)
        except (ValueError, InvalidOperation) as dpe:
            if self._data_type == 'datetime':
                raise InvalidDataValueException("Failed to parse date {} {} '{}'"
                                                .format(self._data_name, self.default_date_format, self._data_value)) from dpe
            else:
                raise InvalidDataValueException("Failed to parse property value {} {} '{}'"
                                                .format(self._data_name, self._data_type, self._data_value)) from dpe
        return converted_field

    @property
    def db_data_value(self):
        return self.from_db_value(self._data_type, self._data_value)

    def compare(self, value):
        #print ("comparing: " + str(value) + " vs " + str(self.typed_data_value))
        #print ("comparing types: " + str(type(value)) + " vs " + str(type(self.typed_data_value)))

        if self._data_type == 'float' or self._data_type == 'double':
            #This will set the prec, which if it's too small can result in InvalidOperation
            compv = self.typed_data_value
            compv_rounded = compv.quantize(value, rounding = ROUND_FLOOR)
            #print ("comparing: " + str(value) + " vs " + str(compv_rounded))
            return compv_rounded == value
        else:
            return self.typed_data_value == value

    @staticmethod
    def from_db_value(db_type, value):

        converted_field = {
            'string': lambda x: BaseDAO._decode(x),
            'integer': lambda x: x,
            'float': lambda x: ServerProperty.float_value(x),
            'double': lambda x: ServerProperty.double_value(x),
            'json': lambda x: x,
            'boolean': lambda x: True if x == 1 else False,
            'datetime': lambda x: x
            }.get(db_type)(value)

        return converted_field

