import connexion
from swagger_server.models.summary import Summary
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from backbone_server.dao.source_dao import SourceDAO
from backbone_server.dao.entity_dao import EntityDAO
import sys
import io
import json

def fields_used_by_entities(propName, propValue, sources=None, include=None):
    """
    fetches entities by property value
    
    :param propName: name of property to search
    :type propName: str
    :param propValue: matching value of property to search
    :type propValue: str
    :param sources: comma separated list of sources
    :type sources: str
    :param include: whether to include all fields (faster) or just those in use
    :type include: str

    :rtype: Fields
    """

    print("report_controller.get_properties_summary")
    edao = EntityDAO()

    fields = edao.fetch_fields_by_property(sources, propName, propValue, include)

    return fields



def get_properties_summary():
    """
    fetches a summary of all the properties
    

    :rtype: Summary
    """

    print("report_controller.get_properties_summary")
    edao = EntityDAO()

    result = edao.get_properties(None)

    return result



def get_property_values_summary(propName, threshold=None):
    """
    fetches a summary of the property values in the source

    :param propName: name of property to search
    :type propName: str
    :param threshold: the lower bound to return
    :type threshold: int

    :rtype: Summary
    """
    print("report_controller.get_property_values_summary")
    edao = EntityDAO()

    result = edao.get_summary_by_property(None, propName, threshold)

    return (result)

def get_source_properties_summary(sourceId):
    """
    fetches a summary of the properties in the source
    
    :param sourceId: ID of source to query
    :type sourceId: str

    :rtype: Summary
    """
    print("report_controller.get_source_properties_summary")
    edao = EntityDAO()

    result = edao.get_properties(sourceId)

    return result

def get_source_property_values_summary(sourceId, propName, threshold=None):
    """
    fetches a summary of the property values in the source
    
    :param sourceId: ID of source to query
    :type sourceId: str
    :param propName: name of property to search
    :type propName: str
    :param threshold: the lower bound to return
    :type threshold: int

    :rtype: Summary
    """
    print("report_controller.get_source_property_values_summary")
    edao = EntityDAO()

    result = edao.get_summary_by_property(sourceId, propName, threshold)

    return (result)


def get_summary():
    """
    fetches a summary of the records in the db


    :rtype: Summary
    """
    print("report_controller.get_summary")
    sd = SourceDAO()

    result = sd.get_report_count_by_source()

    return result
