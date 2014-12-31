"""

Refactorings to do in Eclipse:

@todo: Finish meets()

@todo: Copy docstring signature from ProjectDispatchInterface into cases.
@todo: Rename interface --> OpenProjectCaseInterface
@todo: Rename cases to the style --> OpenProjectFrom{{}}
@todo: Rename dispatch_check --> matches
@todo: Rename form_command --> command
@todo: Add fallback to dispatcher --> if no matches, call subl {_string}
@todo: Add __call__ to cases - should open sublime appropriately


@todo: Refactor out --> interfaces.py
@todo: Refactor out --> errors.py
@todo: Refactor out --> dispatcher.py
@todo: Refactor out --> cases.py
@todo: Refactor out --> support.py
@todo: Write __all__ for each file
"""

import os
import abc
import subprocess


class ProjectDispatchInterface(object):
    """
    Interface for dispatching on the input cases.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def dispatch_check(cls, _string, *args, **kwargs):
        """
        @type: _string: str
        @returns: bool
        """
        return NotImplemented

    @abc.abstractmethod
    def form_command(cls, _string, *args, **kwargs):
        """
        @type: _string: str
        @returns: str
        """
        return NotImplemented

    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is ProjectDispatchInterface:
            if meets(subclass, cls):
                return True
        return NotImplemented


def meets(obj, interface):
    """
    @type: obj: object
    @type: interface: abc.ABCMeta
    @rtype: bool
    """
    return bool(list(missing_abstracts(obj, interface)))
    if list(missing_abstracts(obj, interface)):
        return False
    else:
        return True


def missing_abstracts(obj, interface):
    """
    @type: obj: object
    @type: interface: abc.ABCMeta
    @rtype: str
    """
    for name in interface.__abstractmethods__:
        if not has_concrete_method(obj, name):
            yield name


def has_concrete_method(obj, name):
    """
    @type: obj: object
    @type: name: str
    @returns: bool
    """
    if hasattr(obj, name):
        return is_abstract_method(getattr(obj, name))
    else:
        return False


def is_abstract_method(method):
    return getattr(method, '__isabstractmethod__', False)


#======================================================
# Class Implementations (~Cases for dispatcher)
#======================================================
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
        return is_sublime_project_file(_string)

    @classmethod
    def form_command(cls, _string):
        """
        @type: _string: str
        @rtype: str
        """
        return sublime_project_command(_string)


class OpenFromProjectName(object):
    """
    Input is project file, in standard directory for sublime-project files.
    """
    PROJECTS_DIRECTORY = "Library/Application Support/Sublime Text 3/Packages/User/Projects"

    @classmethod
    def dispatch_check(cls, _string, projects_directory=None):
        if projects_directory is None:
            projects_directory = cls.PROJECTS_DIRECTORY
        return in_projects_directory(_string, projects_directory)

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

    @classmethod
    def project_path(cls, name, directory=None):
        """
        Assumes project directory exists
        """
        if directory is None:
            directory = cls.PROJECTS_DIRECTORY
        return form_project_path(name, directory)


class OpenFromDirectory(object):
    @classmethod
    def dispatch_check(cls, _string):
        return os.path.isdir(_string)


#===================================================
# Dispatcher
#===================================================
class sublp(object):
    """
    Generic-function/dispatcher-function for sublp commandline function.
    """
    cases = [
        OpenFromProjectFilePath,
        OpenFromDirectory,
        OpenFromProjectName,
    ]

    def __new__(cls, _string):
        return cls.__call__(_string)

    def __call__(cls, _string):
        case = cls.match(_string)
        cls.invoke(case, _string)

    @classmethod
    def match(cls, _string):
        """
        Finds case class which matches the input.
        @type: _string: str
        @returns: ProjectDispatchInterface
        """
        for case in cls.cases:
            if case.dispatch_check(_string):
                return case

    @classmethod
    def invoke(cls, case, _string):
        """
        @type: case: ProjectDispatchInterface
        @returns: None
        """
        command = case.form_command(_string)
        subprocess.call(command, shell=True)


#===================================================
# Exceptions
#===================================================
class SublpException(Exception):
    pass


class ProjectNotFoundError(SublpException, IOError):
    pass


class ProjectsDirectoryNotFoundError(SublpException, IOError):
    pass



class ValueMeta(abc.ABCMeta):
    """
    ~ABCMeta, but allows __instancecheck__ to be cleanly overwritten.
    @todo: Copy this into an interface-related package
    """

    def __instancecheck__(cls, instance):
        if hasattr(cls, '__instancecheck__'):
            return cls.__instancecheck__(instance)
        else:
            return abc.ABCMeta.__instancecheck__(cls, instance)

    def __subclasscheck__(cls, subclass):
        if hasattr(cls, '__subclasscheck__'):
            return cls.__subclasscheck__(subclass)
        else:
            return abc.ABCMeta.__subclasscheck__(cls, subclass)


class ExistingDirectory(str):
    __metaclass__ = ValueMeta

    @classmethod
    def __instancecheck__(cls, instance):
        if isinstance(instance, basestring):
            if os.path.isdir(instance):
                return True
        return False


#===================================================
# Support Functions
#===================================================
def form_project_path(name, directory):
    """

    """
    if not os.path.isdir(directory):
        raise ProjectsDirectoryNotFoundError(str.format(
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
        raise ProjectNotFoundError(str.format(
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
