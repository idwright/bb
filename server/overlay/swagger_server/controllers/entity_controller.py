import connexion
from swagger_server.models.inline_response_201 import InlineResponse201
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

    :rtype: List[InlineResponse201]
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

    :rtype: InlineResponse201
    """
    return 'do some magic!'
