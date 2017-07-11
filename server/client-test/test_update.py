from __future__ import print_function
from copy import copy, deepcopy
import swagger_client
from swagger_client.rest import ApiException
from test_base import TestBase



class TestUpdate(TestBase):


    def test_update_property(self):

        try:
            api_instance = swagger_client.SourceApi()
            test_id = self._example_id_prop.data_value

            original = api_instance.download_source_entity('test', test_id)
            entity_id = original.entity_id
            new_entity = deepcopy(original)
            new_prop = copy(self.get_test_prop())

            updated_value = 'Updated value'
            found = False
            for prop in new_entity.values:
                if prop == new_prop:
                    prop.data_value = updated_value
                    found = True

            self.assertTrue(found, "did not find test entity in correct state:" + repr(new_entity))

            entity_api = swagger_client.EntityApi()

            response = entity_api.update_entity(entity_id, new_entity)

            found = False
            for prop in response.values:
                if prop.source == new_prop.source and prop.data_name == new_prop.data_name:
                    self.assertEqual(prop.data_value, updated_value,
                                     "Value not updated from {} to {}".format(updated_value, prop.data_value))
                    found = True

            self.assertTrue(found, "did not find updated property:" + repr(new_prop))

            response = entity_api.update_entity(entity_id, original)

        except ApiException as error:
            self.fail("Exception when calling EntityApi->update_entity: %s\n" % error)


    """
    """
    def create_date_test_entity(self, new_value):

        # create an instance of the API class
        api_instance = swagger_client.SourceApi()
        try:
            api_instance.upload_source('test_date', 'test_target.txt',
                                       additional_metadata='test_date.json')

            original = self.find_entity(api_instance, 'test_date', 'PH0042-C')
            entity_id = original.entity_id

            new_entity = deepcopy(original)
            old_prop = None
            found = False
            for prop in new_entity.values:
                if prop.data_name == 'batch_arrived':
                    old_prop = copy(prop)
                    self.assertEqual(prop.data_type, "datetime")
                    self.assertEqual(prop.data_value, "2009-04-16 00:00:00", "Date value mismatch")
                    prop.data_value = new_value
                    found = True

            self.assertTrue(found, "did not find test entity in correct state:" + repr(new_entity))
        except ApiException as error:
            self.fail("Exception when calling SourceApi->upload_source: %s\n" % error)

        return entity_id, original, new_entity, old_prop

    """
    """
    def test_update_date(self):
        new_value = "2017-07-08 15:54:30"
        entity_id, original, new_entity, old_prop = self.create_date_test_entity(new_value)

        try:
            entity_api = swagger_client.EntityApi()

            response = entity_api.update_entity(entity_id, new_entity)

            found = False
            for prop in response.values:
                if prop.source == old_prop.source and prop.data_name == old_prop.data_name:
                    self.assertEqual(prop.data_value, new_value)
                    found = True

            self.assertTrue(found, "did not find updated property")
            response = entity_api.update_entity(entity_id, original)
        except ApiException as error:
            self.fail("Exception when calling SourceApi->upload_source: %s\n" % error)


    """
    """
    def test_update_date_fail(self):
        new_value = "2017-07-38 15:54:30"
        entity_id, original, new_entity, old_prop = self.create_date_test_entity(new_value)

        try:
            entity_api = swagger_client.EntityApi()

            with self.assertRaises(Exception) as context:
                response = entity_api.update_entity(entity_id, new_entity)

            self.assertEqual(context.exception.status, 422, repr(context))

        except ApiException as error:
            self.fail("Exception when calling SourceApi->upload_source: %s\n" % error)
