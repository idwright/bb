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
        self._example_id_prop = swagger_client.ModelProperty()
        self._example_id_prop.data_name = 'id'
        self._example_id_prop.data_value = '1'
        self._example_id_prop.data_type = 'integer'
        self._example_id_prop.source = self._testSource
        self._example_id_prop.identity = True
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
        props.append(self._example_id_prop)

        entity.values = props

        try:
                response = api_instance.upload_entity(self._testSource, entity)
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
        try:
            response = api_instance.upload_source('bulk_test', 'test_records', additional_metadata='test_metadata.json')
        except ApiException as e:
            print (repr(entity))
            print("Exception when calling EntityApi->upload_entity: %s\n" % e)

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
            response = api_instance.download_source_entity('test', '123456789')
            self.assertIsNone(response)
        except ApiException as e:
            print (repr(entity))
            print("Exception when calling EntityApi->upload_entity: %s\n" % e)

    """
    """
    def test_update_simple_entity(self):

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

            entity_id = response.entity_id
            new_entity = response

            new_prop = swagger_client.ModelProperty(data_name='Added property', \
                                     data_type='string', \
                                     data_value='Added property value', \
                                     source=self._testSource, identity=False)

            new_entity.values.append(new_prop)

            entity_api = swagger_client.EntityApi()

            response = entity_api.update_entity(entity_id, new_entity)
            print(repr(response))
            self.assertEqual(entity_id, response.entity_id)

            found = False
            for prop in response.values:
                if (prop == new_prop):
                    found = True

            self.assertTrue(found, "Added property not found")
        except ApiException as e:
            print (repr(entity))
            print("Exception when calling EntityApi->upload_entity: %s\n" % e)

