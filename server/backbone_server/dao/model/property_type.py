# coding: utf-8

"""
    Backbone

"""


from pprint import pformat
from six import iteritems
import re


class PropertyType(object):

    def __init__(self, ident=None, prop_name=None, prop_type='string', prop_order=None, source=None,
                 identity=False, versionable=True):
        """
        PropertyType - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'ident': 'int',
            'prop_name': 'str',
            'prop_type': 'str',
            'prop_order': 'int',
            'source': 'str',
            'identity': 'bool',
            'versionable': 'bool'
        }

        self.attribute_map = {
            'ident': 'ident',
            'prop_name': 'prop_name',
            'prop_type': 'prop_type',
            'prop_order': 'prop_order',
            'source': 'source',
            'identity': 'identity',
            'versionable': 'versionable'
        }

        self._ident = ident
        self._prop_name = prop_name
        self._prop_type = prop_type
        self._prop_order = prop_order
        self._source = source
        self._identity = identity
        self._versionable = versionable

    @property
    def ident(self):
        """
        Gets the ident of this PropertyType.

        :return: The ident of this PropertyType.
        :rtype: int
        """
        return self._ident

    @ident.setter
    def ident(self, ident):
        """
        Sets the ident of this PropertyType.

        :param ident: The ident of this PropertyType.
        :type: int
        """

        self._ident = ident

    @property
    def prop_name(self):
        """
        Gets the prop_name of this PropertyType.
        The name of the property

        :return: The prop_name of this PropertyType.
        :rtype: str
        """
        return self._prop_name

    @prop_name.setter
    def prop_name(self, prop_name):
        """
        Sets the prop_name of this PropertyType.
        The name of the property

        :param prop_name: The prop_name of this PropertyType.
        :type: str
        """
        if prop_name is None:
            raise ValueError("Invalid value for `prop_name`, must not be `None`")

        self._prop_name = prop_name

    @property
    def prop_type(self):
        """
        Gets the prop_type of this PropertyType.

        :return: The prop_type of this PropertyType.
        :rtype: str
        """
        return self._prop_type

    @prop_type.setter
    def prop_type(self, prop_type):
        """
        Sets the prop_type of this PropertyType.

        :param prop_type: The prop_type of this PropertyType.
        :type: str
        """
        allowed_orders = ["string", "integer", "float", "double", "boolean", "json", "datetime"]
        if prop_type not in allowed_orders:
            raise ValueError(
                "Invalid value for `prop_type` ({0}), must be one of {1}"
                .format(prop_type, allowed_orders)
            )

        self._prop_type = prop_type

    @property
    def prop_order(self):
        """
        Gets the prop_order of this PropertyType.

        :return: The prop_order of this PropertyType.
        :rtype: int
        """
        return self._prop_order

    @prop_order.setter
    def prop_order(self, prop_order):
        """
        Sets the prop_order of this PropertyType.

        :param prop_order: The prop_order of this PropertyType.
        :type: int
        """

        self._prop_order = prop_order

    @property
    def source(self):
        """
        Gets the source of this PropertyType.

        :return: The source of this PropertyType.
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """
        Sets the source of this PropertyType.

        :param source: The source of this PropertyType.
        :type: str
        """
        if source is None:
            raise ValueError("Invalid value for `source`, must not be `None`")

        self._source = source

    @property
    def identity(self):
        """
        Gets the identity of this PropertyType.
        If this an identity column

        :return: The identity of this PropertyType.
        :rtype: bool
        """
        return self._identity

    @identity.setter
    def identity(self, identity):
        """
        Sets the identity of this PropertyType.
        If this an identity column

        :param identity: The identity of this PropertyType.
        :type: bool
        """

        self._identity = identity

    @property
    def versionable(self):
        """
        Gets the versionable of this PropertyType.
        If this an versionable column

        :return: The versionable of this PropertyType.
        :rtype: bool
        """
        return self._versionable

    @versionable.setter
    def versionable(self, versionable):
        """
        Sets the versionable of this PropertyType.
        If this an versionable column

        :param versionable: The versionable of this PropertyType.
        :type: bool
        """

        self._versionable = versionable

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
        if not isinstance(other, PropertyType):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
