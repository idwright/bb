from swagger_server.models.property import Property


class ServerProperty(Property):

    def __init__(self, data_name: str=None, data_type: str='string', data_value: str=None, source:
              str=None, identity: bool=False):
        Property.__init__(self, data_name=data_name, data_type=data_type,
                          data_value=data_value, source=source, identity=identity)

        self.swagger_types['type_id'] = 'integer'
        self._type_id = None

    def __hash__(self):
        return hash(repr(self.to_dict()))

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
            'datetime': "string_value",
        }.get(self._data_type, 'string_value')

        return data_field

    @property
    def typed_data_value(self):
        converted_field = {
            'string': lambda x: x,
            'integer': lambda x: None if x is None or x.lower() == "null" or x == '' else int(x),
            'float': lambda x: float(x),
            'double': lambda x: float(x),
            'json': lambda x: x,
            'boolean': lambda x: 1 if x.lower() == 'true' else 0,
            'datetime': lambda x: None if x is None or x.lower() == "null" or x == '' else x,
            }.get(self._data_type)(self._data_value)

        return converted_field

    @property
    def db_data_value(self):
        return self.from_db_value(self._data_type, self._data_value)

    def from_db_value(self, db_type, value):

        converted_field = {
            'string': lambda x: x.decode('utf-8'),
            'integer': lambda x: x,
            'float': lambda x: x,
            'double': lambda x: x,
            'json': lambda x: x,
            'boolean': lambda x: True if x == 1 else False,
            'datetime': lambda x: x,
            }.get(db_type)(value)

        return converted_field

