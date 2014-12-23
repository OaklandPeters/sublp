"""
Class implementations for sublp.
These are essentially cases for the dispatcher function.

@todo: Change these to be instanced, by passing in
"""
from __future__ import absolute_import

import os

from sublp import support
from sublp import interfaces

NullType = (type(None), )




class New_OpenFromProjectFilePath(interfaces.ProjectDispatchInterface):
    """
    New draft of OpenFromProjectFilePath
    """
    def __init__(self, *args, **kwargs):
        self.set_options(*args, **kwargs)

    # @property
    # def matches(self):
    def dispatch_check(self):
        return support.is_sublime_project_file(self._string)

    # @property
    # def command(self):
    def form_command(self):
        return support.sublime_project_command(self._string)

class New_OpenFromProjectName(interfaces.ProjectDispatchInterface):
    """
    New draft of OpenFromProjectName
    """
    def __init__(self, projects_directory=None):
        self.projects_directory = projects_directory
    @property
    def projects_directory(self):
        if not hasattr(self, '_projects_directory'):
            self._projects_directory =
        return self._projects_directory
    @projects_directory.setter
    def projects_directory(self, value):
        if isinstance(value, NullType):
            self._projects_directory =





class OpenFromProjectFilePath(object):
    """
    Input is path to project file.
    """
    @classmethod
    def dispatch_check(cls, _string):
        """
        @type: _string: str
        @rtype: bool
        """
        return support.is_sublime_project_file(_string)

    @classmethod
    def form_command(cls, _string):
        """
        @type: _string: str
        @rtype: str
        """
        return support.sublime_project_command(_string)


class OpenFromProjectName(object):
    """
    Input is project file, in standard directory for sublime-project files.
    """
    PROJECTS_DIRECTORY = "Library/Application Support/Sublime Text 3/Packages/User/Projects"

    @classmethod
    def dispatch_check(cls, _string, projects_directory=None):
        if projects_directory is None:
            projects_directory = cls.PROJECTS_DIRECTORY
        return support.in_projects_directory(_string, projects_directory)

    @classmethod
    def form_command(cls, _string, projects_directory=None):
        """
        @type: _string: str
        @type: projects_directory: NoneType or str
        @rtype: str
        """
        if projects_directory is None:
            projects_directory = cls.PROJECTS_DIRECTORY
        project_path = os.path.join(projects_directory, _string)
        return support.sublime_project_command(project_path)

    @classmethod
    def project_path(cls, name, directory=None):
        """
        Assumes project directory exists
        """
        if directory is None:
            directory = cls.PROJECTS_DIRECTORY
        return support.form_project_path(name, directory)


class OpenFromDirectory(object):
    @classmethod
    def dispatch_check(cls, _string):
        return os.path.isdir(_string)
