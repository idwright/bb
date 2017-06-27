# coding: utf-8

"""
    Backbone

"""


from pprint import pformat
from six import iteritems
import re



class AssociationType(object):

    def __init__(self, ident=None, assoc_name=None, assoc_type='parent-child'):
        """
        AssociationType - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'ident': 'int',
            'assoc_name': 'str',
            'assoc_type': 'str',
            'key': 'str',
            'source': 'str',
            'target': 'str'
        }

        self.attribute_map = {
            'ident': 'ident',
            'assoc_name': 'assoc_name',
            'assoc_type': 'assoc_type',
            'prop_order': 'prop_order',
            'key': 'key',
            'source': 'source',
            'target': 'target'
        }

        self._ident = ident
        self._assoc_name = assoc_name
        if assoc_type is None:
            assoc_type = 'parent-child'
        self._assoc_type = assoc_type

    @property
    def ident(self):
        """
        Gets the ident of this AssociationType.

        :return: The ident of this AssociationType.
        :rtype: int
        """
        return self._ident

    @ident.setter
    def ident(self, ident):
        """
        Sets the ident of this AssociationType.

        :param ident: The ident of this AssociationType.
        :type: int
        """

        self._ident = ident

    @property
    def assoc_name(self):
        """
        Gets the assoc_name of this AssociationType.
        The name of the property

        :return: The assoc_name of this AssociationType.
        :rtype: str
        """

        if self._assoc_name:
            return self._assoc_name
        else:
            return self._key + "_" + self._source + "_" + self._target

    @assoc_name.setter
    def assoc_name(self, assoc_name):
        """
        Sets the assoc_name of this AssociationType.
        The name of the property

        :param assoc_name: The assoc_name of this AssociationType.
        :type: str
        """
        if assoc_name is None:
            raise ValueError("Invalid value for `assoc_name`, must not be `None`")

        self._assoc_name = assoc_name

    @property
    def assoc_type(self):
        """
        Gets the assoc_type of this AssociationType.

        :return: The assoc_type of this AssociationType.
        :rtype: str
        """
        return self._assoc_type

    @assoc_type.setter
    def assoc_type(self, assoc_type):
        """
        Sets the assoc_type of this AssociationType.

        :param assoc_type: The assoc_type of this AssociationType.
        :type: str
        """
        allowed_orders = ["parent-child", "sibling", "backbone", "system"]
        if assoc_type not in allowed_orders:
            raise ValueError(
                "Invalid value for `assoc_type` ({0}), must be one of {1}"
                .format(assoc_type, allowed_orders)
            )

        self._assoc_type = assoc_type


    @property
    def key(self):
        """
        Gets the key of this AssociationType.
        The name of the property

        :return: The key of this AssociationType.
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """
        Sets the key of this AssociationType.
        The name of the property

        :param key: The key of this AssociationType.
        :type: str
        """
        if key is None:
            raise ValueError("Invalid value for `key`, must not be `None`")

        self._key = key

    @property
    def source(self):
        """
        Gets the source of this AssociationType.
        The name of the property

        :return: The source of this AssociationType.
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """
        Sets the source of this AssociationType.
        The name of the property

        :param source: The source of this AssociationType.
        :type: str
        """
        if source is None:
            raise ValueError("Invalid value for `source`, must not be `None`")

        self._source = source

    @property
    def target(self):
        """
        Gets the target of this AssociationType.
        The name of the property

        :return: The target of this AssociationType.
        :rtype: str
        """
        return self._target

    @target.setter
    def target(self, target):
        """
        Sets the target of this AssociationType.
        The name of the property

        :param target: The target of this AssociationType.
        :type: str
        """
        if target is None:
            raise ValueError("Invalid value for `target`, must not be `None`")

        self._target = target
    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, AssociationType):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
