from swagger_server.models.source_relationship import SourceRelationship 


class BulkLoadSourceRelationship(SourceRelationship):

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
    def assoc_type_id(self) -> int:
        """
        Gets the identity of this Property.
        If this an identity column

        :return: The identity of this Property.
        :rtype: bool
        """
        return self._assoc_type_id

    @assoc_type_id.setter
    def assoc_type_id(self, assoc_type_id: int):
        """
        Sets the identity of this Property.
        If this an identity column

        :param identity: The identity of this Property.
        :type identity: bool
        """

        self._assoc_type_id = assoc_type_id

