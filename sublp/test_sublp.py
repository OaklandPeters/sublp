import os
import unittest
import pdb

from . import dispatcher
from . import errors
from . import dispatch_cases
from . import interfaces
from . import configuration
from . import support

# Set correct directory for testing
file_dir = support.normalize_path(os.path.split(__file__)[0])
if not os.getcwd() == file_dir:
    os.chdir(file_dir)


class InterfaceTests(unittest.TestCase):
    def test_ProjectDispatchInterface(self):
        def meets_dispatcher(case):
            return issubclass(case, interfaces.OpenProjectCaseInterface)

        for case in dispatcher.Sublp.cases:
            self.assertTrue(meets_dispatcher(case))

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
        self.case1 = dispatch_cases.OpenProjectFromFilePath()
        self.case2 = dispatch_cases.OpenProjectFromName(
            projects_directory=self.projects_directory
        )
        self.case3 = dispatch_cases.OpenProjectFromDirectory()
        self.case4 = dispatch_cases.OpenProjectFallback()

    def check_case_match(self, case, name):
        return case.matches(name)

    def matches1(self, name):
        return self.case1.matches(
            name
        )
    def matches2(self, name):
        return self.case2.matches(
            name
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
        case = dispatch_cases.OpenProjectFromFilePath()

        self.assertEqual(case.matches(_string), True)
        expected = "subl --project \"test_bypath/bypath.sublime-project\""
        command = case.command(_string)
        self.assertEqual(command, expected)

    def test_OpenFromProjectName(self):
        """OpenProjectFromName.command()"""
        _string = "byname"
        projects_directory = "test_standard_projects_directory/"
        case = dispatch_cases.OpenProjectFromName(
            projects_directory=projects_directory
        )

        self.assertEqual(case.matches(_string), True)
        path = os.path.join(projects_directory, _string+".sublime-project")
        expected = "subl --project \"{0}\"".format(path)
        command = case.command(_string)
        self.assertEqual(command, expected)

    def test_OpenFromDirectory(self):
        """OpenProjectFromDirectory.command()"""
        _string = "test_project_directory"
        case = dispatch_cases.OpenProjectFromDirectory()

        self.assertEqual(case.matches(_string), True)
        path = os.path.join(_string, 'bydir'+".sublime-project")
        expected = "subl --project \"{0}\"".format(path)
        command = case.command(_string)
        self.assertEqual(command, expected)

    def test_OpenProjectFallback(self):
        """OpenProjectFallback.command()"""
        _string = "no_project_file"
        case = dispatch_cases.OpenProjectFallback()

        self.assertEqual(case.matches(_string), True)
        expected = (
            'subl --project "/Users/opeters/Library/Application Support/'
            'Sublime Text 3/Packages/User/Projects/'
            'no_project_file.sublime-project" '
            '"/Users/opeters/Documents/workspace/sublp/sublp/no_project_file"'
        )
        command = case.command(_string)
        self.assertEqual(command, expected)


class DispatcherTests(unittest.TestCase):

    def compare_matcher(self, name, case):
        result = dispatcher.Sublp.match(name)
        self.assertEqual(result, case)

    def test_file_path(self):
        self.compare_matcher(
            name=os.path.join("test_bypath", "bypath"),
            case=dispatcher.Sublp.OpenProjectFromFilePath
        )

    def test_in_projects(self):
        case = dispatcher.Sublp.OpenProjectFromName
        case.projects_directory = "test_standard_projects_directory"
        self.compare_matcher(
            name="byname",
            case=case
        )

    def test_in_directory(self):
        self.compare_matcher(
            name="test_project_directory",
            case=dispatcher.Sublp.OpenProjectFromDirectory
        )

    def test_fallback(self):
        name = "no_project_file"
        path = support.form_project_path(
            name, configuration.PROJECTS_DIRECTORY
        )
        if os.path.exists(path):
            os.remove(path)
        self.compare_matcher(
            name=name,
            case=dispatcher.Sublp.fallback
        )


class FallbackTests(unittest.TestCase):
    """
    @todo: Distribute these into the above TestCases OR:
    @todo: Split above TestCases into sections, based on dispatcher case
    """
    directory = 'test_blank_dir'
    name = 'createit'
    workspace = os.path.join(directory, name+'.sublime-workspace')
    project = os.path.join(directory, name+'.sublime-project')
    case = dispatch_cases.OpenProjectFallback()

    def setUp(self):
        if not os.path.isdir(self.directory):
            os.mkdir(self.directory)
        if os.path.isfile(self.project):
            os.mkdir(self.project)
        if os.path.isfile(self.workspace):
            os.remove(self.workspace)

    def test_matcher(self):
        self.assertTrue(self.case.matches(self.directory))
        self.assertTrue(self.case.matches(
            os.path.join("test_bypath", "bypath.sublime-project"))
        )
        self.assertFalse(self.case.matches("bypath"))

    def test_command(self):
        expected = (
            'subl --project "/Users/opeters/Library/Application Support/'
            'Sublime Text 3/Packages/User/Projects/'
            'test_blank_dir.sublime-project" '
            '"/Users/opeters/Documents/workspace/sublp/sublp/test_blank_dir"'
        )
        cmd = self.case.command(self.directory)
        self.assertEqual(cmd, expected)

    def test_dispatcher(self):
        # Should confirm that the dispatcher returns this case
        
        result = dispatcher.Sublp.match(self.directory)
        case = dispatcher.Sublp.OpenProjectFallback
        self.assertEqual(result, case)



if __name__ == "__main__":
    unittest.main()
