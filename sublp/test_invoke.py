"""
Opener tests - opens SublimeText
Do not run with standard unittests.
"""
import os
import unittest

import dispatch_cases
import dispatcher
import support

# Set correct directory for testing
file_dir = support.normalize_path(os.path.split(__file__)[0])
if not os.getcwd() == file_dir:
    os.chdir(file_dir)

class InvokeTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_OpenFromProjectFilePath(self):  #pylint:disable=C0103
        """Open based on path to project file"""
        _string = os.path.join("test_bypath", "bypath")
        case = dispatch_cases.OpenProjectFromFilePath()

        self.assertTrue(case.matches(_string))
        dispatcher.Sublp.invoke(case, _string)

    def test_OpenFromProjectName(self):  #pylint:disable=C0103
        """Open based on name of project - contained in standard
        projects directory."""
        _string = "byname"
        projects_directory = "test_standard_projects_directory/"
        case = dispatch_cases.OpenProjectFromName(
            projects_directory=projects_directory
        )

        self.assertTrue(case.matches(_string))
        dispatcher.Sublp.invoke(case, _string)

    def test_OpenFromDirectory(self):  #pylint:disable=C0103
        """Open based on name of directory containing projects file."""
        _string = "test_project_directory"
        case = dispatch_cases.OpenProjectFromDirectory()

        self.assertTrue(case.matches(_string))
        dispatcher.Sublp.invoke(case, _string)

    def test_OpenProjectFallback(self):  #pylint:disable=C0103
        """Run fallback -- no projects file."""
        _string = "no_project_file"
        case = dispatch_cases.OpenProjectFallback()

        self.assertTrue(case.matches(_string))
        dispatcher.Sublp.invoke(case, _string)



if __name__ == "__main__":
    unittest.main()
