"""
Opener tests - opens SublimeText
Do not run with standard unittests.
"""
import os
import unittest

import dispatch_cases
import sublp


def test_OpenFromProjectFilePath():  #pylint:disable=C0103
    """Open based on path to project file"""
    _string = os.path.join("test_bypath", "bypath")
    case = dispatch_cases.OpenProjectFromFilePath()

    assert(case.matches(_string))
    sublp.Sublp.invoke(case, _string)

def test_OpenFromProjectName():  #pylint:disable=C0103
    """Open based on name of project - contained in standard
    projects directory."""
    _string = "byname"
    projects_directory = "test_standard_projects_directory/"
    case = dispatch_cases.OpenProjectFromName(
        projects_directory=projects_directory
    )

    assert(case.matches(_string))
    sublp.Sublp.invoke(case, _string)

def test_OpenFromDirectory():  #pylint:disable=C0103
    """Open based on name of directory containing projects file."""
    _string = "test_project_directory"
    case = dispatch_cases.OpenProjectFromDirectory()

    assert(case.matches(_string))
    sublp.Sublp.invoke(case, _string)

def test_OpenProjectFallback():  #pylint:disable=C0103
    """Run fallback -- no projects file."""
    _string = "no_project_file"
    case = dispatch_cases.OpenProjectFallback()

    assert(case.matches(_string))
    sublp.Sublp.invoke(case, _string)



if __name__ == "__main__":
    tests = [
        test_OpenFromProjectFilePath,
        test_OpenFromProjectName,
        test_OpenFromDirectory,
        test_OpenProjectFallback
    ]

    print("tests[0]()")
    import pdb
    pdb.set_trace()
    print()
