"""
Class Implementations (~Cases for dispatcher)
"""
import sys
import os

import interfaces
import support
import errors

__all__ = [
    'OpenProjectFromFilePath',
    'OpenProjectFromName',
    'OpenProjectFromDirectory',
    'OpenProjectFallback'
]


class OpenProjectFromFilePath(interfaces.OpenProjectCaseInterface):
    """
    Input is path to project file.
    """

    def matches(self, _string):
        """
        @type: _string: str
        @rtype: bool
        """

        path = support.ensure_end(_string, '.sublime-project')
        return support.is_sublime_project_file(path)

    def command(self, _string):
        """
        @type: _string: str
        @rtype: str
        """

        path = support.ensure_end(_string, '.sublime-project')
        return support.sublime_project_command(path)


class OpenProjectFromName(interfaces.OpenProjectCaseInterface):
    """
    Attempt to open a project file by looking in a standardized location
    for all project files (usually located in the user's
    SublimeText packages directory).
    """

    class Defaults(object):
        projects_directory = (
            "~/Library/Application Support/Sublime Text 3/Packages/User/Projects"
        )

    def __init__(self, projects_directory=None):
        """
        Input is project file, in standard directory for sublime-project files.
        """

        if projects_directory is None:
            self.projects_directory = self.Defaults.projects_directory
        else:
            self.projects_directory = projects_directory

    def matches(self, _string, projects_directory=None):
        """
        @type: _string: str
        @returns: bool
        """

        if projects_directory is None:
            projects_directory = self.projects_directory
        return support.in_projects_directory(_string, projects_directory)

    def command(self, _string, projects_directory=None):
        """
        @type: _string: str
        @type: projects_directory: NoneType or str
        @rtype: str
        """
        if projects_directory is None:
            projects_directory = self.projects_directory
        path = os.path.join(projects_directory, _string)
        return support.sublime_project_command(path)


class OpenProjectFromDirectory(interfaces.OpenProjectCaseInterface):
    """
    Open project file contained inside a directory.
    Only works if directory contains only one project file.
    """

    def matches(self, _string):
        """
        Predicate. Does input string match this case?
        @type: _string: str
        @returns: bool

        """
        return self._has_single_project_file(_string)

    def command(self, _string):
        """
        Generate bash command string.
        Assumes _has_single_project_file has already been run.
        @type: _string: str
        @rtype: str
        """
        project_files = self._find_project_files(_string)
        try:
            project_file_path = project_files[0]
        except IndexError:
            raise errors.NoProjectFilesFoundError(str.format(
                "No project files found inside directory: {0}",
                _string
            ))
        return support.sublime_project_command(project_file_path)

    def _find_project_files(self, _string):
        """
        Return list of all project files in _string.
        If _string is not a directory, return empty list.
        @type: _string: str
        @rtype: list of str
        """

        if isinstance(_string, interfaces.ExistingDirectory):
            project_names = support.find_project_files(_string)
            project_paths = list(os.path.join(_string, name) for name in project_names)
            return project_paths
        else:
            return []

    def _has_single_project_file(self, directory):
        """
        Predciate. Does directory contain exactly one project file?
        """

        project_files = self._find_project_files(directory)
        return (len(project_files) == 1)


class OpenProjectFallback(interfaces.OpenProjectCaseInterface):
    """
    Fallback case, if no other cases trigger.
    """

    def matches(self, _string):
        """
        @type: _string: str
        @returns: bool
        """

        if isinstance(_string, interfaces.ExistingPath):
            return True
        return False

    def command(self, _string):
        """
        @type: _string: str
        @rtype: str
        """

        return support.sublime_basic_command(_string)
