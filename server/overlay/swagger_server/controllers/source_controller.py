import connexion
from swagger_server.models.api_response import ApiResponse
from swagger_server.models.entity import Entity
from swagger_server.models.source_entity import SourceEntity
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from backbone_server.dao.source_dao import source_dao
import sys
import io
import json

def delete_source_entity(sourceId, sourceEntityId):
    """
    delete_source_entity

    :param sourceId: ID of source to query
    :type sourceId: str
    :param sourceEntityId: ID of entity to fetch
    :type sourceEntityId: str

    :rtype: None
    """
    print("delete_source_entity")
    return 'do some magic!'


def download_source_entity(sourceId, sourceEntityId):
    """
    fetches an entity

    :param sourceId: ID of source to query
    :type sourceId: str
    :param sourceEntityId: ID of entity to fetch
    :type sourceEntityId: str

    :rtype: Entity
    """
    print("download_source_entity:" + sourceId + "/" + sourceEntityId)
    sd = source_dao()

    result = sd.fetch_entity_by_source(sourceId, sourceEntityId)

    print("result:" + repr(result))
    return result


def upload_entity(sourceId, entity):
    """
    uploads an entity

    :param sourceId: ID of source to update
    :type sourceId: str
    :param entity: desc
    :type entity: dict | bytes

    :rtype: ApiResponse
    """
    print("upload_entity1")
    print(repr(entity))
    if connexion.request.is_json:
        print("upload_entity is json")
        print(repr(connexion.request.get_json()))
#        entity = Entity.from_dict(connexion.request.get_json())

    sd = source_dao()

    print("upload_entity2")
    print(repr(entity))
    result = sd.create_source_entity(sourceId, entity)

    return entity


def upload_source(sourceId, dataFile, additionalMetadata=None):
    """
    bulk upload of entities for a given source

    :param sourceId: ID of source to update
    :type sourceId: int
    :param dataFile: file to upload
    :type dataFile: werkzeug.datastructures.FileStorage
    :param additionalMetadata: Additional data to pass to server
    :type additionalMetadata: str

    :rtype: ApiResponse
    """
    print("upload_source")
    data_def = None
    if additionalMetadata:
        data_def = json.load(io.TextIOWrapper(additionalMetadata.stream, encoding='utf-8'))

    sd = source_dao()

    result = sd.load_data(sourceId, data_def, io.TextIOWrapper(dataFile.stream, encoding='utf-8'))
    return result

def upload_source_entity(sourceId, sourceEntityId, body):
    """
    updates an entity

    :param sourceId: ID of source to update
    :type sourceId: str
    :param sourceEntityId: ID of entity to update
    :type sourceEntityId: str
    :param body: 
    :type body: dict | bytes

    :rtype: SourceEntity
    """
    print("upload_source_entity")
    print(repr(body))
#    if connexion.request.is_json:
#        body = SourceEntity.from_dict(connexion.request.get_json())
    sd = source_dao()

    result = sd.update_source_entity(sourceId, sourceEntityId, body)

    return body
