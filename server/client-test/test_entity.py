from __future__ import print_function
from copy import copy, deepcopy
import swagger_client
from swagger_client.rest import ApiException
from test_base import TestBase



class TestEntity(TestBase):




    """
    """
    def test_add_simple_entity_property(self):

        # create an instance of the API class
        api_instance = swagger_client.SourceApi()

        test_id = self._example_id_prop.data_value

        try:
            response = api_instance.download_source_entity('test', test_id)
            self.assertEqual(str(type(response)), "<class 'swagger_client.models.entity.Entity'>")
            found = False
            for prop in response.values:
                if prop == self._example_id_prop:
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
                if prop == new_prop:
                    found = True

            self.assertTrue(found, "Added property not found")
        except ApiException as error:
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

        except ApiException as error:
            self.fail("Exception when calling EntityApi->update_entity: %s\n" % error)


    def test_update_property_multi_reference(self):
       # create an instance of the API class
        api_instance = swagger_client.SourceApi()
        entity_api = swagger_client.EntityApi()

        props = []
        id_prop = copy(self._example_id_prop)
        id_prop.data_value = '2'
        props.append(id_prop)
        new_prop = copy(self.get_test_prop())
        props.append(new_prop)

        entity = swagger_client.SourceEntity(values=props)

        test_id = self._example_id_prop.data_value
        try:
            #Check that there's another entity with new_prop as a value
            other_entity = api_instance.download_source_entity(self._test_source, test_id)
            found = False
            for prop in other_entity.values:
                if prop == new_prop:
                    found = True

            api_instance.upload_entity(self._test_source, entity)

            new_entity = api_instance.download_source_entity(self._test_source, id_prop.data_value)
            updated_value = 'Updated value'

            found = False
            for prop in new_entity.values:
                if prop == new_prop:
                    found = True
                    prop.data_value = updated_value
            self.assertTrue(found, "did not find updated property")

            #Replace the value of new_prop on the entity we just created
            entity_api.update_entity(new_entity.entity_id, new_entity)

            #Check that new_prop on the other_entity hasn't had it's value changed
            other_entity = api_instance.download_source_entity(self._test_source, test_id)
            found = False
            for prop in other_entity.values:
                if prop == new_prop:
                    found = True

            self.assertTrue(found, "Property on original not found")
        except ApiException as error:
            print (repr(error))
            print("Exception when calling EntityApi->upload_entity: %s\n" % error)
            self.fail("Failed {} {} {}\n".format(error.status, error.reason, error.body))

    """
    """
    def test_add_assoc_property(self):

        # create an instance of the API class
        api_instance = swagger_client.SourceApi()

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
                    if prop == new_prop:
                        found = True
                self.assertTrue(found, "Added property not found")

        except ApiException as error:
            self.fail("Exception when calling EntityApi->update_entity: \n")

    def test_duplicate_assoc_property(self):

        try:
            api_instance = swagger_client.SourceApi()

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

        except ApiException as error:
            self.fail("Exception when calling EntityApi->update_entity: \n")
