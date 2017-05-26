import connexion
from swagger_server.models.body import Body
from swagger_server.models.entity import Entity
from swagger_server.models.inline_response_200 import InlineResponse200
from swagger_server.models.inline_response_200_1 import InlineResponse2001
from swagger_server.models.inline_response_201 import InlineResponse201
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from backbone_server.dao.source_dao import source_dao
import sys

def delete_source_entity(sourceId, sourceEntityId):
    """
    delete_source_entity

    :param sourceId: ID of source to query
    :type sourceId: str
    :param sourceEntityId: ID of entity to fetch
    :type sourceEntityId: str

    :rtype: None
    """
    print("delete_source_entity", file=sys.stderr)
    return 'do some magic!'


def download_source_entity(sourceId, sourceEntityId):
    """
    fetches an entity

    :param sourceId: ID of source to query
    :type sourceId: str
    :param sourceEntityId: ID of entity to fetch
    :type sourceEntityId: str

    :rtype: InlineResponse201
    """
    print("download_source_entity", file=sys.stderr)
    sd = source_dao()

    result = sd.fetch_entity_by_source(sourceId, sourceEntityId)

    return result


def upload_entity(sourceId, entity):
    """
    uploads an entity

    :param sourceId: ID of source to update
    :type sourceId: str
    :param entity: desc
    :type entity: dict | bytes

    :rtype: InlineResponse200
    """
    print("upload_entity1", file=sys.stderr)
    print(repr(entity), file=sys.stderr)
    if connexion.request.is_json:
        print("upload_entity is json", file=sys.stderr)
        print(repr(connexion.request.get_json()), file=sys.stderr)
#        entity = Entity.from_dict(connexion.request.get_json())

    sd = source_dao()

    print("upload_entity2", file=sys.stderr)
    print(repr(entity), file=sys.stderr)
    result = sd.create_source_entity(sourceId, entity)

    return entity


def upload_source(sourceId, additionalMetadata=None, file=None):
    """
    bulk upload of entities for a given source
    
    :param sourceId: ID of source to update
    :type sourceId: int
    :param additionalMetadata: Additional data to pass to server
    :type additionalMetadata: str
    :param file: file to upload
    :type file: werkzeug.datastructures.FileStorage

    :rtype: InlineResponse200
    """
    print("upload_source", file=sys.stderr)
    return 'do some magic2!'

def upload_source_entity(sourceId, sourceEntityId, body):
    """
    updates an entity
    
    :param sourceId: ID of source to update
    :type sourceId: str
    :param sourceEntityId: ID of entity to update
    :type sourceEntityId: str
    :param body: 
    :type body: dict | bytes

    :rtype: InlineResponse2001
    """
    print("upload_source_entity", file=sys.stderr)
    print(repr(body), file=sys.stderr)
#    if connexion.request.is_json:
#        body = Entity.from_dict(connexion.request.get_json())
    sd = source_dao()

    result = sd.update_source_entity(sourceId, sourceEntityId, body)

    return body
