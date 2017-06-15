from __future__ import print_function
import unittest
import time
import json
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
from test_base import TestBase



class TestEntity(TestBase):


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

            self.assertEqual(entity_id, response.entity_id)

            found = False
            for prop in response.values:
                if (prop == new_prop):
                    found = True

            self.assertTrue(found, "Added property not found")
        except ApiException as e:
            print (repr(entity))
            print("Exception when calling EntityApi->upload_entity: %s\n" % e)

