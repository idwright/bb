from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
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
            api_instance.upload_entity(self._test_source, entity)
        except ApiException as error:
            print (repr(error))
            print("Exception when calling EntityApi->upload_entity: %s\n" % error)
            self.fail("Failed {} {} {}\n".format(error.status, error.reason, error.body))

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
            api_instance.upload_entity(self._test_source + 'fail', entity)

        self.assertEqual(context.exception.status, 404)



    """
    """
    def test_fetch_simple_entity(self):

        # create an instance of the API class
        api_instance = swagger_client.SourceApi()

        test_id = self._example_id_prop.data_value

        try:

            self.find_entity(api_instance, 'test', test_id)

            #Look for a non-existent entity
            with self.assertRaises(Exception) as context:
                api_instance.download_source_entity('test', '123456789')

            self.assertEqual(context.exception.status, 404)
        except ApiException as error:
            self.fail("Exception when calling EntityApi->upload_entity: %s\n" % error)


