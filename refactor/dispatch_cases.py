"""
Class Implementations (~Cases for dispatcher)
"""
import sys
import os

import interfaces
import support

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
    @classmethod
    def matches(cls, _string):
        """
        @type: _string: str
        @rtype: bool
        """

        path = support.ensure_end(_string, '.sublime-project')
        return support.is_sublime_project_file(path)

    @classmethod
    def command(cls, _string):
        """
        @type: _string: str
        @rtype: str
        """

        path = support.ensure_end(_string, '.sublime-project')
        return support.sublime_project_command(path)


class OpenProjectFromName(interfaces.OpenProjectCaseInterface):
    """
    Input is project file, in standard directory for sublime-project files.
    """
    projects_directory = (
        "~/Library/Application Support/Sublime Text 3/Packages/User/Projects"
    )


    @classmethod
    def matches(cls, _string, projects_directory=None):
        """
        @type: _string: str
        @returns: bool
        """

        if projects_directory is None:
            projects_directory = cls.projects_directory
        return support.in_projects_directory(_string, projects_directory)

    @classmethod
    def get_projects_directory(cls, projects_directory=None):
        """
        @type: projects_directory: str or None
        @rtype: str
        """

        if projects_directory is None:
            return cls.projects_directory
        else:
            return projects_directory


    @classmethod
    def command(cls, _string, projects_directory=None):
        """
        @type: _string: str
        @type: projects_directory: NoneType or str
        @rtype: str
        """
        if projects_directory is None:
            projects_directory = cls.projects_directory
        path = os.path.join(projects_directory, _string)
        return support.sublime_project_command(path)

    @classmethod
    def project_path(cls, name, directory=None):
        """
        Assumes project directory exists
        @type: name: str
        @type: directory: str or None
        @rtype: str
        """
        if directory is None:
            directory = cls.projects_directory
        return support.form_project_path(name, directory)


class OpenProjectFromDirectory(interfaces.OpenProjectCaseInterface):
    """
    Open project file contained inside a directory.
    Only works if directory contains only one project file.
    """
    @classmethod
    def matches(cls, _string):
        """
        Predicate. Does input string match this case?
        @type: _string: str
        @returns: bool

        """
        return cls._has_single_project_file(_string)

    @classmethod
    def command(cls, _string):
        """
        Generate bash command string.
        Assumes _has_single_project_file has already been run.
        @type: _string: str
        @rtype: str
        """

        project_file_path = cls._find_project_files(_string)[0]
        return support.sublime_project_command(project_file_path)

    @classmethod
    def _find_project_files(cls, _string):
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

    @classmethod
    def _has_single_project_file(cls, directory):
        """
        Predciate. Does directory contain exactly one project file?
        """

        project_files = cls._find_project_files(directory)
        return (len(project_files) == 1)


class OpenProjectFallback(interfaces.OpenProjectCaseInterface):
    """
    Fallback case, if no other cases trigger.
    """

    @classmethod
    def matches(cls, _string):
        """
        @type: _string: str
        @returns: bool
        """

        if isinstance(_string, interfaces.ExistingPath):
            return True
        return False

    @classmethod
    def command(cls, _string):
        """
        @type: _string: str
        @rtype: str
        """

        return "sublime "+_string
