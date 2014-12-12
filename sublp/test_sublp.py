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
        import pdb
        pdb.set_trace()
        print()

if __name__ == "__main__":
    #unittest.main()

    word = 'sublp'
    ed = sublp.ExistingDirectory
    print(os.listdir(os.getcwd()))
    #print(ED.__instancecheck__(word))
    print(isinstance(word, ED))


    pdb.set_trace()
    print()
