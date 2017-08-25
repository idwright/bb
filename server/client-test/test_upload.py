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
            api_instance.upload_source('test_source', 'test_source.txt', additional_metadata='test_source.json',
                                       skip_header=True)

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
    """
    """
    def test_replace(self):

        # create an instance of the API class
        api_instance = swagger_client.SourceApi()
        try:
            api_instance.upload_source('test_replace', 'test_replace.txt',
                                       additional_metadata='test_replace.json',
                                       skip_header=True)

            rec1 = self.find_entity(api_instance, 'test_replace', 'Bangladesh')

            for prop in rec1.values:
                if prop.data_name == 'country':
                    self.assertEqual(prop.data_value, "BD")

            rec2 = self.find_entity(api_instance, 'test_replace', 'Sarpang Tar, Sarpang')

            for prop in rec2.values:
                if prop.data_name == 'country':
                    self.assertEqual(prop.data_value, "BT")


        except ApiException as error:
            self.fail("Exception when calling EntityApi->load_source_entities\n")

    """
    """
    def test_transform(self):

        # create an instance of the API class
        api_instance = swagger_client.SourceApi()
        try:
            api_instance.upload_source('test_transform', 'test_source.txt',
                                       additional_metadata='test_transform.json',
                                       skip_header=True)

            rec1 = self.find_entity(api_instance, 'test_transform', '3288_6_nonhuman')

            self.check_implied_target(api_instance, 'alfresco_transform', '1011', rec1, True)
            self.check_implied_target(api_instance, 'sanger_ega_dataset_transform',
                                      '3288_6_nonhuman', rec1, True)

        except ApiException as error:
            self.fail("Exception when calling EntityApi->load_source_entities\n")

    """
    """
    def test_date(self):

        # create an instance of the API class
        api_instance = swagger_client.SourceApi()
        try:
            api_instance.upload_source('test_date', 'test_target.txt',
                                       additional_metadata='test_date.json')

            rec1 = self.find_entity(api_instance, 'test_date', 'PH0042-C')

            for prop in rec1.values:
                if prop.data_name == 'batch_arrived':
                    self.assertEqual(prop.data_type, "datetime")
                    self.assertEqual(prop.data_value, "2009-04-16 00:00:00", "Date value mismatch")
        except ApiException as error:
            self.fail("Exception when calling SourceApi->upload_source: %s\n" % error)

    """
    """
    def test_date_format(self):

        # create an instance of the API class
        api_instance = swagger_client.SourceApi()
        try:
            api_instance.upload_source('date_format', 'combination_keys.txt',
                                       additional_metadata='test_date_format.json')
            rec1 = self.find_entity(api_instance, 'date_format', '1046')

            for prop in rec1.values:
                if prop.data_name == 'collection_date':
                    self.assertEqual(prop.data_type, "datetime")
                    self.assertEqual(prop.data_value, "2008-07-02 00:00:00", "Date value mismatch")
        except ApiException as error:
            self.fail("Exception when calling SourceApi->upload_source: %s\n" % error)

    """
    """
    def test_empty_date(self):
        #Not implemented
        pass

    """
    """
    def test_date_comparison(self):
        #Not implemented
        #Check the modified value is correctly reported
        pass

    """
    """
    def test_date_format_fail(self):

        # create an instance of the API class
        api_instance = swagger_client.SourceApi()
        try:
            with self.assertRaises(Exception) as context:
                api_instance.upload_source('date_format_fail', 'combination_keys.txt',
                                       additional_metadata='test_date_format_fail.json')

            self.assertEqual(context.exception.status, 422, context.exception)

        except ApiException as error:
            self.fail("Exception when calling SourceApi->upload_source: %s\n" % error)

    """
    """
    def test_skip_header(self):

        # create an instance of the API class
        api_instance = swagger_client.SourceApi()
        try:
            skip_default = api_instance.upload_source('header_test_default', 'test_records', additional_metadata='test_metadata.json')
            skip_true = api_instance.upload_source('header_test_true', 'test_records',
                                       additional_metadata='test_metadata.json', skip_header=True)
            skip_false = api_instance.upload_source('header_test_false', 'test_records',
                                       additional_metadata='test_metadata.json', skip_header=False)

            self.assertEqual(skip_default.processed, skip_false.processed)
            self.assertEqual(skip_default.processed, skip_true.processed + 1)

        except ApiException as error:
            self.fail("Exception when calling EntityApi->upload_entity: %s\n" % error)



    """
    """
    def test_update_only(self):

        # create an instance of the API class
        api_instance = swagger_client.SourceApi()
        try:
            update_only = api_instance.upload_source('alfresco_transform', 'alfresco_codes',
                                                      additional_metadata='test_update_only.json',
                                                     update_only=True, skip_header=False)

            self.assertEqual(update_only.modified, 1)
            self.assertEqual(update_only.processed, 4)
            self.assertEqual(update_only.created, 0)

        except ApiException as error:
            self.fail("Exception when calling EntityApi->upload_entity: %s\n" % error)


    """
    """
    def test_update_only_false(self):

        # create an instance of the API class
        api_instance = swagger_client.SourceApi()
        try:
            update_only = api_instance.upload_source('alfresco_transform', 'alfresco_codes',
                                                      additional_metadata='test_update_only.json',
                                                     update_only=False, skip_header=False)

            self.assertEqual(update_only.modified, 0)
            self.assertEqual(update_only.processed, 4)
            self.assertEqual(update_only.created, 3)

        except ApiException as error:
            self.fail("Exception when calling EntityApi->upload_entity: %s\n" % error)
