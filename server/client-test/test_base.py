from __future__ import print_function
import unittest
import swagger_client



class TestBase(unittest.TestCase):

    _test_source = None

    """
    """
    def setUp(self):
        self._test_source = 'test'
        self._example_id_prop = swagger_client.ModelProperty()
        self._example_id_prop.data_name = 'id'
        self._example_id_prop.data_value = '1'
        self._example_id_prop.data_type = 'integer'
        self._example_id_prop.source = self._test_source
        self._example_id_prop.identity = True

    """
    """
    def tearDown(self):
        pass


    def find_entity(self, api_instance, source, entity_id):

        response = api_instance.download_source_entity(source, entity_id)
        self.assertEqual(str(type(response)), "<class 'swagger_client.models.entity.Entity'>")
        found = False
        for prop in response.values:
            if prop.identity and prop.source == source and prop.data_value == entity_id:
                found = True

        self.assertTrue(found, "Did not find example")

        return response

    def check_implied_target(self, api_instance, source_source, source_id, target_entity, implied):

        source_entity = self.find_entity(api_instance, source_source, source_id)

        for prop in source_entity.values:
            if prop.source == 'system' and prop.data_name == 'implied_id':
                self.assertEqual(prop.data_value == 'true', implied)

        found = False
        for assoc in source_entity.refs:
            if assoc.source_id == source_entity.entity_id and \
               assoc.target_id == target_entity.entity_id:
                found = True

        self.assertTrue(found, "Association not found")

        found = False
        for assoc in target_entity.refs:
            if assoc.source_id == source_entity.entity_id and \
               assoc.target_id == target_entity.entity_id:
                found = True

        self.assertTrue(found, "Association not found")
