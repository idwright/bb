from swagger_server.models.property import Property


class BulkLoadProperty(Property):

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

