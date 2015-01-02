import os
import unittest
import pdb

import sublp

class InterfaceTests(unittest.TestCase):
    def test_ProjectDispatchInterface(self):
        def meets_dispatcher(case):
            return issubclass(case, sublp.OpenProjectCaseInterface)

        for case in sublp.sublp.cases:
            self.assert_(meets_dispatcher(case))
        # self.assert_(meets_dispatcher(sublp.OpenProjectFromFilePath))
        # self.assert_(meets_dispatcher(sublp.OpenProjectFromName))
        # self.assert_(meets_dispatcher(sublp.OpenProjectFromDirectory))
        # self.assert_(meets_dispatcher(sublp.OpenProjectFallback))

    def test_ExistingDirectory(self):
        self.assert_(isinstance('test_bypath', sublp.ExistingDirectory))
        self.assert_(not isinstance('_test_bypath', sublp.ExistingDirectory))

        self.assert_(os.path.exists('__init__.py'))
        self.assert_(not isinstance('__init__.py', sublp.ExistingDirectory))


class CaseMatchTests(unittest.TestCase):
    """
    Test .dispatch_check() method for the cases.
    """

    def setUp(self):
        self.projects_directory = "test_standard_projects_directory/"
        self.case1 = sublp.OpenProjectFromFilePath
        self.case2 = sublp.OpenProjectFromName
        self.case3 = sublp.OpenProjectFromDirectory
        self.case4 = sublp.OpenProjectFallback

    def matches1(self, name):
        return self.case1.dispatch_check(
            name
        )
    def matches2(self, name):
        return self.case2.dispatch_check(
            name, projects_directory=self.projects_directory
        )
    def matches3(self, name):
        return self.case3.dispatch_check(
            name
        )
    def matches4(self, name):
        return self.case4.dispatch_check(
            name
        )

    def test_file_path(self):
        name = os.path.join("test_bypath", "bypath")
        self.assertEquals(self.matches1(name), True)
        self.assertEquals(self.matches2(name), False)
        self.assertEquals(self.matches3(name), False)
        self.assertEquals(self.matches4(name), False)

        name = os.path.join("test_bypath", "bypath.sublime-project")
        self.assertEquals(self.matches1(name), True)
        self.assertEquals(self.matches2(name), False)
        self.assertEquals(self.matches3(name), False)
        self.assertEquals(self.matches4(name), True)

    def test_in_projects(self):
        name = "byname"
        self.assertEquals(self.matches1(name), False)
        self.assertEquals(self.matches2(name), True)
        self.assertEquals(self.matches3(name), False)
        self.assertEquals(self.matches4(name), False)

    def test_in_directory(self):
        name = "test_project_directory"
        self.assertEquals(self.matches1(name), False)
        self.assertEquals(self.matches2(name), False)
        self.assertEquals(self.matches3(name), True)
        self.assertEquals(self.matches4(name), True)

    def test_fallback(self):
        name ="no_project_file"
        self.assertEquals(self.matches1(name), False)
        self.assertEquals(self.matches2(name), False)
        self.assertEquals(self.matches3(name), False)
        self.assertEquals(self.matches4(name), True)



class FormCommandTests(unittest.TestCase):
    """
    Test .form_command() method for the cases.
    """
    def setUp(self):
        self.projects_directory = "test_standard_projects_directory/"


    def test_OpenFromProjectFilePath(self):
        """OpenProjectFromFilePath.form_command()"""
        _string = os.path.join("test_bypath", "bypath")
        case = sublp.OpenProjectFromFilePath

        self.assertEqual(case.dispatch_check(_string), True)
        expected = "subl --project test_bypath/bypath.sublime-project"
        command = case.form_command(_string)
        self.assertEqual(command, expected)

    def test_OpenFromProjectName(self):
        """OpenProjectFromName.form_command()"""
        _string = "byname"
        projects_directory = "test_standard_projects_directory/"
        case = sublp.OpenProjectFromName

        self.assertEqual(
            case.dispatch_check(_string, projects_directory=projects_directory),
            True
        )
        expected = ("subl --project test_standard_projects_directory"
                    "/byname.sublime-project")
        command = case.form_command(
            _string, projects_directory=projects_directory
        )
        self.assertEqual(command, expected)

    def test_OpenFromDirectory(self):
        """OpenProjectFromDirectory.form_command()"""
        _string = "test_project_directory"
        case = sublp.OpenProjectFromDirectory

        self.assertEqual(case.dispatch_check(_string), True)
        expected = "subl --project test_project_directory/bydir.sublime-project"
        command = case.form_command(_string)
        self.assertEqual(command, expected)




class DispatcherTests(unittest.TestCase):

    def compare_matcher(self, name, case):
        result = sublp.sublp.match(name)
        self.assertEqual(result, case)

    def test_file_path(self):
        self.compare_matcher(
            name=os.path.join("test_bypath", "bypath"),
            case=sublp.OpenProjectFromFilePath
        )

    def test_in_projects(self):
        from sublp import OpenProjectFromName
        OpenProjectFromName.projects_directory = "test_standard_projects_directory/"
        self.compare_matcher(
            name="byname",
            case=OpenProjectFromName
        )

    def test_in_directory(self):
        self.compare_matcher(
            name="test_project_directory",
            case=sublp.OpenProjectFromDirectory
        )

    def test_fallback(self):
        self.compare_matcher(
            name="no_project_file",
            case=sublp.OpenProjectFallback
        )


if __name__ == "__main__":
    unittest.main()


