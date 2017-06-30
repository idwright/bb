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
