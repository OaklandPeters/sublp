import os
import unittest
import pdb

import sublp
import errors
import dispatch_cases
import interfaces

class InterfaceTests(unittest.TestCase):
    def test_ProjectDispatchInterface(self):
        def meets_dispatcher(case):
            return issubclass(case, interfaces.OpenProjectCaseInterface)

        for case in sublp.Sublp.cases:
            self.assertTrue(meets_dispatcher(case))
        # self.assertTrue(meets_dispatcher(dispatch_cases.OpenProjectFromFilePath))
        # self.assertTrue(meets_dispatcher(dispatch_cases.OpenProjectFromName))
        # self.assertTrue(meets_dispatcher(dispatch_cases.OpenProjectFromDirectory))
        # self.assertTrue(meets_dispatcher(dispatch_cases.OpenProjectFallback))

    def test_ExistingDirectory(self):
        self.assertTrue(isinstance('test_bypath', interfaces.ExistingDirectory))
        self.assertTrue(not isinstance('_test_bypath', interfaces.ExistingDirectory))

        self.assertTrue(os.path.exists('__init__.py'))
        self.assertTrue(not isinstance('__init__.py', interfaces.ExistingDirectory))


class CaseMatchTests(unittest.TestCase):
    """
    Test .matches() method for the cases.
    """

    def setUp(self):
        self.projects_directory = "test_standard_projects_directory/"
        self.case1 = dispatch_cases.OpenProjectFromFilePath
        self.case2 = dispatch_cases.OpenProjectFromName
        self.case3 = dispatch_cases.OpenProjectFromDirectory
        self.case4 = dispatch_cases.OpenProjectFallback

    def matches1(self, name):
        return self.case1.matches(
            name
        )
    def matches2(self, name):
        return self.case2.matches(
            name, projects_directory=self.projects_directory
        )
    def matches3(self, name):
        return self.case3.matches(
            name
        )
    def matches4(self, name):
        return self.case4.matches(
            name
        )

    def test_file_path(self):
        name = os.path.join("test_bypath", "bypath")
        self.assertEqual(self.matches1(name), True)
        self.assertEqual(self.matches2(name), False)
        self.assertEqual(self.matches3(name), False)
        self.assertEqual(self.matches4(name), False)

        name = os.path.join("test_bypath", "bypath.sublime-project")
        self.assertEqual(self.matches1(name), True)
        self.assertEqual(self.matches2(name), False)
        self.assertEqual(self.matches3(name), False)
        self.assertEqual(self.matches4(name), True)

    def test_in_projects(self):
        name = "byname"
        self.assertEqual(self.matches1(name), False)
        self.assertEqual(self.matches2(name), True)
        self.assertEqual(self.matches3(name), False)
        self.assertEqual(self.matches4(name), False)

    def test_in_directory(self):
        name = "test_project_directory"
        self.assertEqual(self.matches1(name), False)
        self.assertEqual(self.matches2(name), False)
        self.assertEqual(self.matches3(name), True)
        self.assertEqual(self.matches4(name), True)

    def test_fallback(self):
        name ="no_project_file"
        self.assertEqual(self.matches1(name), False)
        self.assertEqual(self.matches2(name), False)
        self.assertEqual(self.matches3(name), False)
        self.assertEqual(self.matches4(name), True)



class FormCommandTests(unittest.TestCase):
    """
    Test .command() method for the cases.
    """
    def setUp(self):
        self.projects_directory = "test_standard_projects_directory/"


    def test_OpenFromProjectFilePath(self):
        """OpenProjectFromFilePath.command()"""
        _string = os.path.join("test_bypath", "bypath")
        case = dispatch_cases.OpenProjectFromFilePath

        self.assertEqual(case.matches(_string), True)
        expected = "subl --project test_bypath/bypath.sublime-project"
        command = case.command(_string)
        self.assertEqual(command, expected)

    def test_OpenFromProjectName(self):
        """OpenProjectFromName.command()"""
        _string = "byname"
        projects_directory = "test_standard_projects_directory/"
        case = dispatch_cases.OpenProjectFromName

        self.assertEqual(
            case.matches(_string, projects_directory=projects_directory),
            True
        )
        expected = ("subl --project test_standard_projects_directory"
                    "/byname.sublime-project")
        command = case.command(
            _string, projects_directory=projects_directory
        )
        self.assertEqual(command, expected)

    def test_OpenFromDirectory(self):
        """OpenProjectFromDirectory.command()"""
        _string = "test_project_directory"
        case = dispatch_cases.OpenProjectFromDirectory

        self.assertEqual(case.matches(_string), True)
        expected = "subl --project test_project_directory/bydir.sublime-project"
        command = case.command(_string)
        self.assertEqual(command, expected)




class DispatcherTests(unittest.TestCase):

    def compare_matcher(self, name, case):
        result = sublp.Sublp.match(name)
        self.assertEqual(result, case)

    def test_file_path(self):
        self.compare_matcher(
            name=os.path.join("test_bypath", "bypath"),
            case=dispatch_cases.OpenProjectFromFilePath
        )

    def test_in_projects(self):
        from dispatch_cases import OpenProjectFromName
        OpenProjectFromName.projects_directory = "test_standard_projects_directory/"
        self.compare_matcher(
            name="byname",
            case=OpenProjectFromName
        )

    def test_in_directory(self):
        self.compare_matcher(
            name="test_project_directory",
            case=dispatch_cases.OpenProjectFromDirectory
        )

    def test_fallback(self):
        self.compare_matcher(
            name="no_project_file",
            case=dispatch_cases.OpenProjectFallback
        )


if __name__ == "__main__":
    unittest.main()


