import connexion

from backbone_server.errors.no_such_type_exception import NoSuchTypeException
from backbone_server.errors.duplicate_property_exception import DuplicatePropertyException

from swagger_server.models.entities import Entities
from swagger_server.models.entity import Entity
from swagger_server.models.source_entity import SourceEntity
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime
import logging

from backbone_server.dao.entity_dao import EntityDAO
import sys

def delete_entity(entityId):
    """
    deletes an entity
    
    :param entityId: ID of entity to fetch
    :type entityId: str

    :rtype: None
    """
    return 'do some magic!'


def download_entities_by_property(propName, propValue, start=None, count=None, orderby=None):
    """
    fetches entities by property value

    :param propName: name of property to search
    :type propName: str
    :param propValue: matching value of property to search
    :type propValue: str
    :param start: for pagination start the result set at a record x
    :type start: int
    :param count: for pagination the number of entries to return
    :type count: int
    :param orderby: how to order the result set
    :type orderby: str

    :rtype: Entities
    """
    print("download_entities_by_property")

    result = None
    retcode = 200

    ed = EntityDAO()

    try:
        result = ed.fetch_entities_by_property(None, propName, propValue, start, count, orderby)
    except NoSuchTypeException as t:
        logging.getLogger().error("download_entities_by_property: {}".format(t))
        retcode = 404

    return result, retcode



def download_entity(entityId):
    """
    fetches an entity

    :param entityId: ID of entity to fetch
    :type entityId: str

    :rtype: Entity
    """
    print("download_entity")
    ed = EntityDAO()

    result = ed.fetch_entity_by_id(entityId, None)

    return result

def update_entity(entityId, entity):
    """
    updates an entity

    :param entityId: ID of entity to update
    :type entityId: str
    :param entity:
    :type entity: dict | bytes

    :rtype: Entity
    """
    #print("update_entity", file=sys.stderr)
    if connexion.request.is_json:
      entity = Entity.from_dict(connexion.request.get_json())
      #print(repr(entity))
    ed = EntityDAO()

    retcode = 200
    try:
        retval = ed.update_entity(entity)
    except DuplicatePropertyException as t:
        logging.getLogger().error("update_entity: {}".format(repr(t)))
        retcode = 422
    #print(repr(retval))

    result = ed.fetch_entity_by_id(entityId, None)

    return result, retcode

