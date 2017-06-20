from __future__ import print_function
from copy import deepcopy

from test_base import TestBase
import swagger_client
from swagger_client.rest import ApiException

class TestAssociation(TestBase):


    """
    """
    def test_remove_association(self):

        try:

            entity_api = swagger_client.EntityApi()
            source_api = swagger_client.SourceApi()
            original = source_api.download_source_entity('test_source', '3288_6_nonhuman.bam')

            entity_id = original.entity_id
            new_entity = deepcopy(original)

            updated_value = 'Updated fk value'
            for prop in new_entity.values:
                if prop.data_value == 'PH0042-C':
                    prop.data_value = updated_value


            response = entity_api.update_entity(entity_id, new_entity)

            self.check_implied_target(source_api, 'test_target', updated_value, response, True)

            with self.assertRaises(Exception) as context:
                self.check_implied_target(source_api, 'test_target', 'PH0042-C', response, False)

            self.assertEqual(repr(context.exception),
                             "AssertionError('False is not true : Association not found',)")
        except ApiException as error:
            self.fail("Exception when calling EntityApi->load_source_entities: %s\n" % error)

