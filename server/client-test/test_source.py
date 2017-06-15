from __future__ import print_function
import unittest
import time
import json
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
from test_base import TestBase



class TestSource(TestBase):


    """
    """
    def test_create_simple_entity(self):

        # create an instance of the API class
        api_instance = swagger_client.SourceApi()
        entity = swagger_client.SourceEntity()

        props = []
        props.append(self._example_id_prop)

        entity.values = props

        try:
            response = api_instance.upload_entity(self._testSource, entity)
        except ApiException as e:
            print (repr(e))
            print("Exception when calling EntityApi->upload_entity: %s\n" % e)
            self.fail("Failed {} {} {}\n".format(e.status, e.reason, e.body))

    """
    """
    def test_invalid_source_create_simple_entity(self):

        # create an instance of the API class
        api_instance = swagger_client.SourceApi()
        entity = swagger_client.SourceEntity()

        props = []
        props.append(self._example_id_prop)

        entity.values = props

        with self.assertRaises(Exception) as context:
            api_instance.upload_entity(self._testSource + 'fail', entity)

        self.assertEqual(context.exception.status, 404)


    """
    """
    def test_load_simple_entities(self):

        # create an instance of the API class
        api_instance = swagger_client.SourceApi()
        entity = swagger_client.SourceEntity()
        try:
            response = api_instance.upload_source('bulk_test', 'test_records', additional_metadata='test_metadata.json')
        except ApiException as e:
            fail("Exception when calling EntityApi->upload_entity: %s\n" % e)

    """
    """
    def test_load_combination_key_entities(self):

        # create an instance of the API class
        api_instance = swagger_client.SourceApi()
        entity = swagger_client.SourceEntity()
        try:
            response = api_instance.upload_source('combination_keys', 'combination_keys.txt', additional_metadata='combination_keys.json')
        except ApiException as e:
            print (repr(entity))
            fail("Exception when calling EntityApi->upload_entity: %s\n" % e)

    """
    """
    def test_fetch_simple_entity(self):

        # create an instance of the API class
        api_instance = swagger_client.SourceApi()
        entity = swagger_client.SourceEntity()

        test_id = self._example_id_prop.data_value

        try:
            response = api_instance.download_source_entity('test', test_id)
            self.assertEqual(str(type(response)),"<class 'swagger_client.models.entity.Entity'>")
            found = False
            for prop in response.values:
                if (prop == self._example_id_prop):
                    found = True

            self.assertTrue(found, "Did not find example")


            #Look for a non-existent entity
            with self.assertRaises(Exception) as context:
                response = api_instance.download_source_entity('test', '123456789')

            self.assertEqual(context.exception.status, 404)
        except ApiException as e:
            print (repr(entity))
            fail("Exception when calling EntityApi->upload_entity: %s\n" % e)

