from __future__ import print_function
import unittest
import time
import json
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
from test_base import TestBase



class TestEntity(TestBase):


    def get_test_prop(self):

        new_prop = swagger_client.ModelProperty(data_name='Added property', \
                                 data_type='string', \
                                 data_value='Added property value', \
                                 source=self._testSource, identity=False)
        return new_prop



    """
    """
    def test_add_simple_entity_property(self):

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

            new_prop = self.get_test_prop()

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
            self.fail("Exception when calling EntityApi->update_entity: ")

    def test_duplicate_property(self):

        try:
            api_instance = swagger_client.SourceApi()
            test_id = self._example_id_prop.data_value

            response = api_instance.download_source_entity('test', test_id)
            entity_id = response.entity_id
            new_entity = response
            new_prop = self.get_test_prop()

            new_entity.values.append(new_prop)

            entity_api = swagger_client.EntityApi()

            with self.assertRaises(Exception) as context:
                response = entity_api.update_entity(entity_id, new_entity)

            self.assertEqual(context.exception.status, 422)

        except ApiException as e:
            self.fail("Exception when calling EntityApi->update_entity: %s\n" % e)

    """
    """
    def test_add_assoc_property(self):

        # create an instance of the API class
        api_instance = swagger_client.SourceApi()
        entity = swagger_client.SourceEntity()

        test_id = self._example_id_prop.data_value

        try:
            response = api_instance.download_source_entity('test_target', 'PH0042-C')

            entity_id = response.entity_id
            new_entity = response

            new_prop = self.get_test_prop()

            for assoc in new_entity.refs:
                assoc.values.append(new_prop)

            entity_api = swagger_client.EntityApi()

            response = entity_api.update_entity(entity_id, new_entity)

            self.assertEqual(entity_id, response.entity_id)

            for assoc in new_entity.refs:
                found = False
                for prop in assoc.values:
                    if (prop == new_prop):
                        found = True
                self.assertTrue(found, "Added property not found")

        except ApiException as e:
            self.fail("Exception when calling EntityApi->update_entity: \n")

    def test_duplicate_assoc_property(self):

        try:
            api_instance = swagger_client.SourceApi()
            test_id = self._example_id_prop.data_value

            response = api_instance.download_source_entity('test_target', 'PH0042-C')
            entity_id = response.entity_id
            new_entity = response
            new_prop = self.get_test_prop()

            for assoc in new_entity.refs:
                assoc.values.append(new_prop)

            entity_api = swagger_client.EntityApi()

            with self.assertRaises(Exception) as context:
                response = entity_api.update_entity(entity_id, new_entity)

            self.assertEqual(context.exception.status, 422)

        except ApiException as e:
            self.fail("Exception when calling EntityApi->update_entity: \n")
