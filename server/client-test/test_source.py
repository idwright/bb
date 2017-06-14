from __future__ import print_function
import unittest
import time
import json
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint



class TestSource(unittest.TestCase):

    """
    """
    def setUp(self):
        self._testSource = 'test'
        pass

    """
    """
    def tearDown(self):
        pass

    """
    """
    def test_create_simple_entity(self):

        # create an instance of the API class
        api_instance = swagger_client.SourceApi()
        entity = swagger_client.SourceEntity()

        props = []
        prop = swagger_client.ModelProperty()
        prop.data_name = 'id'
        prop.data_value = '1'
        prop.data_type = 'integer'
        prop.source = self._testSource
        prop.identity = True
        props.append(prop)

        entity.values = props

        try:
                response = api_instance.upload_entity(self._testSource, entity)
                print(repr(response))
        except ApiException as e:
            print (repr(entity))
            print("Exception when calling EntityApi->upload_entity: %s\n" % e)

        self.assertEqual(1,1)


    """
    """
    def test_load_simple_entities(self):

        # create an instance of the API class
        api_instance = swagger_client.SourceApi()
        entity = swagger_client.SourceEntity()
        #data_file = open('test_records', 'r')
        try:
            response = api_instance.upload_source('bulk_test', 'test_records', additional_metadata='test_metadata.json')
            print(repr(response))
        except ApiException as e:
            print (repr(entity))
            print("Exception when calling EntityApi->upload_entity: %s\n" % e)

