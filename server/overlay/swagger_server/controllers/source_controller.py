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

#import cProfile


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
    if connexion.request.is_json:
        ent = Entity.from_dict(connexion.request.get_json())

    sd = source_dao()

    result = sd.create_source_entity(sourceId, ent)

    return entity


def upload_source(sourceId, dataFile, additionalMetadata=None, update_only=None):
    """
    bulk upload of entities for a given source
    
    :param sourceId: ID of source to update
    :type sourceId: str
    :param dataFile: file to upload
    :type dataFile: werkzeug.datastructures.FileStorage
    :param additionalMetadata: Additional data to pass to server
    :type additionalMetadata: str
    :param update_only: Only update existing records e.g. for filling in implied values
    :type update_only: bool

    :rtype: ApiResponse
    """
    print("upload_source")
    data_def = None
    if additionalMetadata:
        data_def = json.load(io.TextIOWrapper(additionalMetadata.stream, encoding='utf-8'))

    sd = source_dao()

    input_stream = io.TextIOWrapper(dataFile.stream, encoding='utf-8')

#    profile = cProfile.Profile()
#    profile.enable()
    result = sd.load_data(sourceId, data_def, input_stream)
#    profile.disable()
#    profile.print_stats()
#    profile.dump_stats('upload_source_stats.cprof')
#$ pyprof2calltree -k -i upload_source_stats.cprof

    return ApiResponse(code=result)
