import connexion
from swagger_server.models.api_response import ApiResponse
from swagger_server.models.entity import Entity
from swagger_server.models.source_entity import SourceEntity
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from backbone_server.dao.source_dao import SourceDAO
from backbone_server.dao.entity_dao import EntityDAO
import sys
import json

from backbone_server.errors.incomplete_combination_key_exception import IncompleteCombinationKeyException
from backbone_server.errors.no_id_exception import NoIdException
from backbone_server.errors.duplicate_id_exception import DuplicateIdException
from backbone_server.errors.invalid_id_exception import InvalidIdException

#import cProfile

def download_source_entities_by_property(sourceId, propName, propValue, start=None, count=None,
                                           orderby=None):
    """
    fetches entities by property value for a given source
    
    :param sourceId: ID of source to query
    :type sourceId: str
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
    print("download_source_entities_by_property")

    result = None
    retcode = 200

    ed = EntityDAO()

    try:
        result = ed.fetch_entities_by_property(sourceId, propName, propValue, start, count, orderby)
    except NoSuchTypeException as t:
        logging.getLogger().error("download_entities_by_property: {}".format(t))
        retcode = 404

    return result, retcode


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
    sd = SourceDAO()

    try:
        result = sd.fetch_entity_by_source(sourceId, sourceEntityId)
    except InvalidIdException as e:
        return repr(e), 404 #Unprocessable entity
    except NoIdException as e:
        #No identity key specified for this source
        return repr(e), 422 #Unprocessable entity
    except IncompleteCombinationKeyException as e:
        #Source uses a combination key, which means it can't be retrieved via this method
        return repr(e), 409 #Unprocessable entity
    #print("result:" + repr(result))
    return result, 200


def upload_entity(sourceId, entity):
    """
    uploads an entity
    
    :param sourceId: ID of source to which the entity should belong
    :type sourceId: str
    :param entity: desc
    :type entity: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        entity = SourceEntity.from_dict(connexion.request.get_json())
    return 'do some magic!'

    sd = SourceDAO()

    try:
        result = sd.create_source_entity(sourceId, ent)
    except InvalidIdException as e:
        return repr(e), 404 #Unprocessable entity
    except NoIdException as e:
        return repr(e), 422 #Unprocessable entity
    except IncompleteCombinationKeyException as e:
        return repr(e), 422 #Unprocessable entity
    except DuplicateIdException as e:
        return repr(e), 409 #Conflict

    return result, 201


def upload_source(sourceId, dataFile, additionalMetadata=None, update_only=None):
    """
    bulk upload of entities for a given source
    
    :param sourceId: ID of source to update
    :type sourceId: str
    :param dataFile: file to upload
    :type dataFile: werkzeug.datastructures.FileStorage
    :param additionalMetadata: Additional data to pass to server
    :type additionalMetadata: werkzeug.datastructures.FileStorage
    :param updateOnly: Only update existing records e.g. for filling in implied values
    :type updateOnly: bool

    :rtype: ApiResponse
    """
    print("upload_source")
    data_def = None
    if additionalMetadata:
        data_def = json.load(io.TextIOWrapper(additionalMetadata.stream, encoding='utf-8'))

    sd = SourceDAO()

    input_stream = io.TextIOWrapper(dataFile.stream, encoding='utf-8')

#    profile = cProfile.Profile()
#    profile.enable()
    result = sd.load_data(sourceId, data_def, input_stream)
#    profile.disable()
#    profile.print_stats()
#    profile.dump_stats('upload_source_stats.cprof')
#$ pyprof2calltree -k -i upload_source_stats.cprof

    return ApiResponse(code=result)
