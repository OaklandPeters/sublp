import os
import unittest
import pdb

import sublp

os.chdir('..')

class InterfaceTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_ExistingDirectory(self):
        self.assert_(isinstance('sublp', sublp.ExistingDirectory))
        self.assert_(not isinstance('sublp_', sublp.ExistingDirectory))

if __name__ == "__main__":
    unittest.main()
