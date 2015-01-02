"""
Support functions.
"""
import os

import errors

def form_project_path(name, directory):
    """
    @type: name: str
    @type: directory: name
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
    return False  # fallthrough condition


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

def find_project_files(directory):
    """
    @type: directory: str
    @rtype: iter of str
    """
    for name in os.listdir(directory):
        if name.endswith('.sublime-project'):
            yield name

def to_paths(iterable, prefix=None):
    """
    @type: iterable: iter of str
    @param: iterable: File names or partial paths of files.
    @type: prefix: str or None
    @param: prefix: Directory to use as prefix. If None, uses os.getcwd()
    @rtype: iter of str
    @returns: Names with path prefixes joined.
    to_paths(find_project_files(_string), _string)
    """
    if prefix is None:
        prefix = os.getcwd()
    for name in iterable:
        yield os.path.join(prefix, name)

def has_project_file(directory):
    """
    Predicate. Does directory contain a sublime project file
    @type: directory: str
    @rtype: bool
    """
    return bool(list(find_project_files(directory)))