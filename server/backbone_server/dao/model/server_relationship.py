from swagger_server.models.relationship import Relationship 


class ServerRelationship(Relationship):

    @property
    def assoc_type(self) -> str:
        """
        Gets the association type of this Relationship.

        :return: The association type of this Relationship.
        :rtype: str
        """
        return self._assoc_type

    @assoc_type.setter
    def assoc_type(self, assoc_type: str):
        """
        Sets the association type of this Relationship.

        :param assoc_type: The association type of this Relationship.
        :type assoc_type: str
        """

        self._assoc_type = assoc_type

    @property
    def assoc_type_id(self) -> int:
        """
        Gets the association type id of this Relationship.

        :return: The association type id of this Relationship.
        :rtype: int
        """
        return self._assoc_type_id

    @assoc_type_id.setter
    def assoc_type_id(self, assoc_type_id: int):
        """
        Sets the association type id of this Relationship.

        :param assoc_type_id: The association type id of this Relationship.
        :type assoc_type_id: int
        """

        self._assoc_type_id = assoc_type_id

