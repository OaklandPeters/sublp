"""
Support functions for sublp.
"""
from __future__ import absolute_import
import os

from sublp import errors

__all__ = [
    'form_project_path',
    'sublime_project_command',
    'is_sublime_project_file',
    'in_projects_directory',
    'ensure_end'
]

def form_project_path(name, directory):
    """
    @type: name: str
    @type: directory: str
    @rtype: str
    """
    if not os.path.isdir(directory):
        raise errors.ProjectsDirectoryNotFoundError(str.format(
        ))
    project_name = ensure_end(name, '.sublime-project')
    return os.path.join(directory, project_name)


def sublime_project_command(path):
    """
    @type: path: str
    @returns: str
    """
    project_path = ensure_end(path, '.sublime-project')
    if not os.path.isfile(project_path):
        raise errors.ProjectNotFoundError(str.format(
            "No Sublime Text project file found at {0}",
            project_path
        ))
    command = str.format(
        "subl --project {project_path}",
        project_path=project_path
    )
    return command


def is_sublime_project_file(path):
    """
    @type: path: str
    @returns: bool
    """
    if os.path.exists(path):
        if os.path.isfile(path):
            if path.endswith('sublime-project'):
                return True
    else:
        return False


def in_projects_directory(name, directory):
    """
    @type: name: str - project name, with or without extension
    @type: directory: str - project directory
    @returns: bool
    """
    project_name = ensure_end(name, '.sublime-project')

    if os.path.exists(directory):
        contents = os.listdir(directory)
        if project_name in contents:
            return True
    else:
        return False


def ensure_end(haystack, ending):
    """
    @type: haystack: str
    @type: ending: str
    @returns: str
    """
    if haystack.endswith(ending):
        return haystack
    else:
        return haystack+ending
