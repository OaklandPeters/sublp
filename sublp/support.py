"""
Support functions.
"""
import os
import json

from . import errors

__all__ = [
    "ensure_end",
    "errors",
    "find_project_files",
    "form_project_path",
    "form_workspace_path",
    "has_project_file",
    "in_projects_directory",
    "is_sublime_project_file",
    "sublime_project_command",
    "to_paths"
]

def form_project_path(name, directory):
    """
    Create path for sublime project file from file name and directory.
    @type: name: str
    @type: directory: str
    @rtype: str
    """
    if not os.path.isdir(directory):
        raise errors.ProjectsDirectoryNotFoundError(str.format(
            "'{0}' is not an existing directory.", directory
        ))
    project_name = ensure_end(name, '.sublime-project')
    return os.path.join(directory, project_name)

def form_workspace_path(name, directory):
    """
    Create path for sublime workspace file from file name and directory.
    @type: name: str
    @type: directory: str
    @rtype: str
    """
    if not os.path.isdir(directory):
        raise errors.ProjectsDirectoryNotFoundError(str.format(
            "'{0}' is not an existing directory.", directory
        ))
    workspace_name = ensure_end(name, '.sublime-workspace')
    return os.path.join(directory, workspace_name)

def sublime_project_command(path):
    """
    Form bash command to open a Sublime Text project.
    @type: path: str
    @rtype: str
    """
    project_path = ensure_end(path, '.sublime-project')
    if not os.path.isfile(project_path):
        raise errors.ProjectNotFoundError(str.format(
            "No Sublime Text project file found at {0}",
            project_path
        ))
    command = str.format(
        "subl --project \"{project_path}\"",
        project_path=project_path
    )
    return command

def sublime_targeted_project_command(path, target):
    """
    Form bash command to open a Sublime Text project.
    @type: path: str
    @type: target: str
    @rtype: str
    """
    project_path = ensure_end(path, '.sublime-project')
    if not os.path.isfile(project_path):
        raise errors.ProjectNotFoundError(str.format(
            "No Sublime Text project file found at {0}",
            project_path
        ))
    command = str.format(
         "subl --project \"{project_path}\" \"{project_target}\"",
        project_path=project_path, project_target=target
    )
    return command

def sublime_basic_command(path):
    """
    Form bash command to open file in Sublime Text.
    @type: path: str
    @rtype: str
    """
    return str.format(
        "subl \"{path}\"",
        path=path
    )

def is_sublime_project_file(path):
    """
    Does path refer to a sublime project file?
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
    Is {name}.sublime-project contained in directory?
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
    Ensure that string ends with specific ending.
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
    Return .sublime-project files contained in directory.
    @type: directory: str
    @rtype: iter of str
    """
    for name in os.listdir(directory):
        if name.endswith('.sublime-project'):
            yield name

def to_paths(iterable, prefix=None):
    """
    Convert file names to absolute paths.
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

def normalize_path(path):
    """
    @type: path: str
    @rtype: str
    """
    return os.path.abspath(os.path.normpath(path))

def write_json(path, values):
    """
    Write values to a JSON file. May overwrite current.
    @type: path: FilePath
    @type: values: collections.Mapping
    @rtype: None
    """

    with open(path, 'w') as json_file:
        json.dump(values, json_file)
