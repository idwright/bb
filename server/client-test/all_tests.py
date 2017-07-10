import unittest

from test_source import TestSource
from test_upload import TestUpload
from test_entity import TestEntity
from test_association import TestAssociation


def my_suite():
    suite = unittest.TestSuite()
    result = unittest.TestResult()
    suite.addTest(unittest.makeSuite(TestSource))
    suite.addTest(unittest.makeSuite(TestUpload))
    suite.addTest(unittest.makeSuite(TestEntity))
    suite.addTest(unittest.makeSuite(TestAssociation))
    runner = unittest.TextTestRunner()
    print(runner.run(suite))

my_suite()
