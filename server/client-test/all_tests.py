import unittest

from test_source import TestSource
from test_entity import TestEntity


def my_suite():
    suite = unittest.TestSuite()
    result = unittest.TestResult()
    suite.addTest(unittest.makeSuite(TestSource))
    suite.addTest(unittest.makeSuite(TestEntity))
    runner = unittest.TextTestRunner()
    print(runner.run(suite))

my_suite()
