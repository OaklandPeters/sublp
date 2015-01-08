"""
Class Implementations (~Cases for dispatcher)
"""
import sys
import os

import interfaces
import support
import errors
import configuration

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
        projects_directory = configuration.PROJECTS_DIRECTORY

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
        name = support.ensure_end(_string, '.sublime-project')
        return (name in self._dir_contents())
#        return support.in_projects_directory(_string, projects_directory)

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

    def _dir_contents(self):
        """
        List contents of projects_directory.
        @rtype: list of str
        """
        if self.projects_directory is not None:
            if os.path.exists(self.projects_directory):
                return os.listdir(self.projects_directory)
        # Fallthrough condition
        return []

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


class OpenProjectFallbackCreateNew(interfaces.OpenProjectCaseInterface):
    """
    Fallback condition.
    Creates new project and workspace files and opens that project.
    ... this probably requires an existing folder
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

        name = self.parse_name(_string)
        directory = self.parse_directory(_string)
        self.create_project(name, directory)
        self.create_workspace(name, directory)
        project_path = support.form_project_path(name, directory)
        return support.sublime_targeted_project_command(project_path, _string)

    def parse_name(self, _string):
        """
        Return the name which should be used for the project file.
        """

        path = support.normalize_path(_string)
        if os.path.isdir(path):
            # final part of directory
            return self._get_final_dir(path)
        elif os.path.isfile(path):
            # file name, without path or extension
            return self._get_file_no_ext(path)
        else:
            raise errors.SublpException(
                "{0} does not know how to find project name for '{1}'.",
                type(self).__name__, path
            )

    def parse_directory(self, _string):
        """
        Return directory where project files should be contained.
        """

        # Default projects directory
        if configuration.DEFAULT_TO_PROJECTS_DIRECTORY:
            if os.path.isdir(configuration.PROJECTS_DIRECTORY):
                return configuration.PROJECTS_DIRECTORY
        # Extract destination directory from input
        path = support.normalize_path(_string)
        if os.path.isdir(path):
            return path
        elif os.path.isfile(path):
            return os.path.split(path)[0]
        else:
            raise errors.SublpException(
                "{0} does not know how to find directory for '{1}'.",
                type(self).__name__, path
            )

    def create_project(self, name, directory):
        """
        @type: name: str
        @type: directory: str
        @rtype: None
        """

        path = support.form_project_path(name, directory)
        support.write_json(path, {})

    def create_workspace(self, name, directory):
        """
        @type: name: str
        @type: directory: str
        @rtype: None
        """

        path = support.form_workspace_path(name, directory)
        support.write_json(path, {})

    def _get_final_dir(self, path):
        """
        Returns final directory contained in path.
        Path should *not* be a file.
        @type: path: str
        @param: path: a directory
        @rtype: str
        """
        return os.path.basename(support.normalize_path(path))

    def _get_file_no_ext(self, path):
        """
        @type: path: str
        @rtype: str
        """
        _, _fileext = os.path.split(path)
        return os.path.splitext(_fileext)[0]


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
