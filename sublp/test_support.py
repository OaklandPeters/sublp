"""
Tests the interfaces file -- which varies between py2 and py3
Particularly tests the 'meets' related functions
"""
import sys
import os
import unittest
import pdb

from . import dispatch_cases as cases
from . import support
from . import dispatcher

# Set correct directory for testing
FILE_DIR = support.normalize_path(os.path.split(__file__)[0])
if not os.getcwd() == FILE_DIR:
    os.chdir(FILE_DIR)



class InterfacesTests(object):
    """Generic between python 2 and python 3."""
    def test_meets(self):
        meetings = [
            (case, self.interfaces.meets(case, self.interface))
            for case in dispatcher.Sublp.cases
        ]

        for case in dispatcher.Sublp.cases:
            self.assertTrue(self.interfaces.meets(case, self.interface))
        self.assertFalse(self.interfaces.meets(self.FakeCase, self.interface))

    def test_missing(self):
        case = cases.OpenProjectFallback
        wrong = self.FakeCase
        interface = self.interfaces.OpenProjectCaseInterface

        missing_case = list(self.interfaces.missing_abstracts(case, interface))
        missing_wrong = list(self.interfaces.missing_abstracts(wrong, interface))

        self.assertEqual(missing_case, [])
        self.assertEqual(missing_wrong, ['matches', 'command'])



if sys.version_info[0] < 3:
    from . import py2
    class Py2Tests(unittest.TestCase, InterfacesTests):
        def setUp(self):
            self.interfaces = py2
            self.interface = self.interfaces.OpenProjectCaseInterface

            class FakeCase(self.interface):
                def __init__(self):
                    pass
            self.FakeCase = FakeCase
else:
    from . import py3
    class Py3Tests(unittest.TestCase, InterfacesTests):
        def setUp(self):
            self.interfaces = py3
            self.interface = self.interfaces.OpenProjectCaseInterface

            class FakeCase(self.interface):
                def __init__(self):
                    pass
            self.FakeCase = FakeCase
        

if __name__ == "__main__":
    unittest.main()
