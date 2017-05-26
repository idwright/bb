import connexion
from swagger_server.models.entities import Entities
from swagger_server.models.entity import Entity
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from backbone_server.dao.entity_dao import entity_dao
import sys


def download_entities_by_property(propName, propValue):
    """
    fetches entities by property value
    
    :param propName: name of property to search
    :type propName: str
    :param propValue: matching value of property to search
    :type propValue: str

    :rtype: Entities
    """
    print("download_entities_by_property", file=sys.stderr)
    ed = entity_dao()

    result = ed.fetch_entities_by_property(propName, propValue)

    return result



def download_entity(entityId):
    """
    fetches an entity
    
    :param entityId: ID of entity to fetch
    :type entityId: str

    :rtype: Entity
    """
    print("download_entity", file=sys.stderr)
    ed = entity_dao()

    result = ed.fetch_entity_by_id(entityId, None)

    return result

