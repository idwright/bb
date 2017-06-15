from __future__ import print_function
import unittest
import time
import json
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint



class TestBase(unittest.TestCase):

    """
    """
    def setUp(self):
        self._testSource = 'test'
        self._example_id_prop = swagger_client.ModelProperty()
        self._example_id_prop.data_name = 'id'
        self._example_id_prop.data_value = '1'
        self._example_id_prop.data_type = 'integer'
        self._example_id_prop.source = self._testSource
        self._example_id_prop.identity = True
        pass

    """
    """
    def tearDown(self):
        pass

