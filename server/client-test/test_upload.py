from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from test_base import TestBase



class TestUpload(TestBase):


    """
    """
    def test_load_simple_entities(self):

        # create an instance of the API class
        api_instance = swagger_client.SourceApi()
        try:
            api_instance.upload_source('bulk_test', 'test_records', additional_metadata='test_metadata.json')
        except ApiException as error:
            self.fail("Exception when calling EntityApi->upload_entity: %s\n" % error)

    """
    """
    def test_load_combination_key_entities(self):

        # create an instance of the API class
        api_instance = swagger_client.SourceApi()
        try:
            api_instance.upload_source('combination_keys', 'combination_keys.txt', additional_metadata='combination_keys.json')
        except ApiException as error:
            self.fail("Exception when calling EntityApi->upload_entity: %s\n" % error)


    """
    """
    def test_load_source_entities(self):

        # create an instance of the API class
        api_instance = swagger_client.SourceApi()
        try:
            api_instance.upload_source('test_source', 'test_source.txt', additional_metadata='test_source.json')

            rec1 = self.find_entity(api_instance, 'test_source', '3288_6_nonhuman.bam')
            self.check_implied_target(api_instance, 'test_target', 'PH0042-C', rec1, True)
            self.check_implied_target(api_instance, 'alfresco', '1011-PF-KH-SU', rec1, True)

            rec2 = self.find_entity(api_instance, 'test_source', '5380_2_nonhuman.bam')
            self.check_implied_target(api_instance, 'alfresco', '1010-PF-TH-ANDERSON', rec2, True)
            self.check_implied_target(api_instance, 'test_target', 'PD0123-C', rec2, True)

        except ApiException as error:
            self.fail("Exception when calling EntityApi->load_source_entities\n")

    """
    """
    def test_load_target_entities(self):

        # create an instance of the API class
        api_instance = swagger_client.SourceApi()
        try:
            api_instance.upload_source('test_target', 'test_target.txt', additional_metadata='test_target.json')

            rec1 = self.find_entity(api_instance, 'test_source', '3288_6_nonhuman.bam')
            self.check_implied_target(api_instance, 'test_target', 'PH0042-C', rec1, False)
            self.check_implied_target(api_instance, 'alfresco', '1011-PF-KH-SU', rec1, True)

            rec2 = self.find_entity(api_instance, 'test_source', '5380_2_nonhuman.bam')
            self.check_implied_target(api_instance, 'test_target', 'PD0123-C', rec2, False)
            self.check_implied_target(api_instance, 'alfresco', '1010-PF-TH-ANDERSON', rec2, True)

        except ApiException as error:
            self.fail("Exception when calling EntityApi->load_source_entities: %s\n" % error)

