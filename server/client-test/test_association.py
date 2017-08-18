from __future__ import print_function
from copy import deepcopy

from test_base import TestBase
import swagger_client
from swagger_client.rest import ApiException

class TestAssociation(TestBase):


    """
    """
    def test_remove_s_association(self):

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

    """
    """
    def test_remove_t_association(self):

        try:

            entity_api = swagger_client.EntityApi()
            source_api = swagger_client.SourceApi()

            target_id = 'PD0123-C'
            original = source_api.download_source_entity('test_target', target_id)

            entity_id = original.entity_id
            new_entity = deepcopy(original)

            updated_value = 'Updated target fk value'
            for prop in new_entity.values:
                if prop.data_value == target_id and prop.identity:
                    prop.data_value = updated_value


            response = entity_api.update_entity(entity_id, new_entity)

            source = source_api.download_source_entity('test_source', '5380_2_nonhuman.bam')
            #There should still be an association but to a different record and the target will be implied now
            self.check_implied_target(source_api, 'test_target', target_id, source, True)

            #There should not be an association to the original record
            with self.assertRaises(Exception) as context:
                self.check_implied_target(source_api, 'test_target', updated_value, response, False)

            self.assertEqual(repr(context.exception),
                             "AssertionError('False is not true : Association not found',)")
        except ApiException as error:
            self.fail("Exception when calling EntityApi->load_source_entities: %s\n" % error)

    """
    """
    def test_rmerge_source_entities(self):

        # create an instance of the API class
        api_instance = swagger_client.SourceApi()
        try:
            api_instance.upload_source('test_merge', 'test_source.txt',
                                       additional_metadata='test_merge.json', skip_header=True)

            rec1 = self.find_entity(api_instance, 'test_merge', '3288_6_nonhuman.bam')
            rec2 = self.find_entity(api_instance, 'test_target', 'PH0042-C')
            self.assertEqual(rec1.entity_id,rec2.entity_id)

        except ApiException as error:
            self.fail("Exception when calling EntityApi->load_source_entities\n")

    """
    """
    def test_mismatch_prop_type(self):

        # create an instance of the API class
        api_instance = swagger_client.SourceApi()
        try:
            with self.assertRaises(Exception) as context:
                api_instance.upload_source('test_mismatch', 'test_prop_mismatch.txt',
                                       additional_metadata='test_prop_mismatch.json', skip_header=True)

            self.assertEqual(context.exception.status, 422)
            self.assertEqual(context.exception.body,
                             '"'+ "InvalidDataValueException('Error inserting property alfresco alfresco_code integer 0 - probably type mismatch',)" + '"\n')


        except ApiException as error:
            self.fail("Exception when calling EntityApi->load_source_entities\n")

