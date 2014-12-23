"""

Refactorings to do in Eclipse:

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
class OpenFromProjectFilePath(ProjectDispatchInterface):
    """
    Input is path to project file.
    """
    @classmethod
    def dispatch_check(cls, _string):
        """
        @type: _string: str
        @rtype: bool
        """
        path = ensure_end(_string, '.sublime-project')
        return is_sublime_project_file(path)

    @classmethod
    def form_command(cls, _string):
        """
        @type: _string: str
        @rtype: str
        """
        path = ensure_end(_string, '.sublime-project')
        return sublime_project_command(path)


class OpenFromProjectName(ProjectDispatchInterface):
    """
    Input is project file, in standard directory for sublime-project files.
    """
    projects_directory = (
        "~/Library/Application Support/Sublime Text 3/Packages/User/Projects"
    )


    @classmethod
    def dispatch_check(cls, _string, projects_directory=None):
        if projects_directory is None:
            projects_directory = cls.projects_directory
        return in_projects_directory(_string, projects_directory)

    @classmethod
    def get_projects_directory(cls, projects_directory=None):
        if projects_directory is None:
            return cls.projects_directory
        else:
            return projects_directory


    @classmethod
    def form_command(cls, _string, projects_directory=None):
        """
        @type: _string: str
        @type: projects_directory: NoneType or str
        @rtype: str
        """
        if projects_directory is None:
            projects_directory = cls.projects_directory
        path = os.path.join(projects_directory, _string)
        return sublime_project_command(path)

    @classmethod
    def project_path(cls, name, directory=None):
        """
        Assumes project directory exists
        """
        if directory is None:
            directory = cls.projects_directory
        return form_project_path(name, directory)


class OpenFromDirectory(ProjectDispatchInterface):
    """
    Open project file contained inside a directory.
    Only works if directory contains only one project file.
    """
    @classmethod
    def dispatch_check(cls, _string):
        return cls._has_single_project_file(_string)

    @classmethod
    def form_command(cls, _string):
        """
        Assumes _has_single_project_file has already been run
        """
        project_file_path = cls._find_project_files(_string)[0]
        return sublime_project_command(project_file_path)

    @classmethod
    def _find_project_files(cls, _string):
        """
        Return list of all project files in _string.
        If _string is not a directory, return empty list.
        @type: _string: str
        @rtype: list of str
        """
        if isinstance(_string, ExistingDirectory):
            project_names = find_project_files(_string)
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


class OpenFromFallback(ProjectDispatchInterface):
    """Fallback case, if no other cases trigger."""
    @classmethod
    def dispatch_check(cls, _string):
        if isinstance(_string, ExistingPath):
            return True
        return False

    @classmethod
    def form_command(cls, _string):
        return "sublime "+_string


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
        OpenFromFallback
    ]

    def __new__(cls, _string):
        return cls.__call__(_string)

    @classmethod
    def __call__(cls, _string):
        """Primary flow-control.
        @type: _string: str
        @rtype: None
        """
        case = cls.match(_string)
        cls.invoke(case, _string)

    @classmethod
    def match(cls, _string):
        """
        Finds case class which matches the input.
        @type: _string: str
        @returns: ProjectDispatchInterface
        """
        _string = cls._validate_string(_string)

        for case in cls.cases:
            if case.dispatch_check(_string):
                return case

        raise UnmatchedInputString(str.format(
            "Cannot find an appropriate sublime project file for '{0}'.",
            _string
        ))

    @classmethod
    def invoke(cls, case, _string):
        """
        @type: case: ProjectDispatchInterface
        @returns: None
        """
        _string = cls._validate_string(_string)
        command = case.form_command(_string)
        subprocess.call(command, shell=True)

    @classmethod
    def _validate_string(cls, _string):
        """Validate input string."""
        if not isinstance(_string, basestring):
            raise TypeError("'_string' must be instance of basestring.")
        return _string


#===================================================
# Exceptions
#===================================================
class SublpException(Exception):
    """Root exception type for sublp module."""
    pass


class ProjectNotFoundError(SublpException, IOError):
    """
    Raised by sublp when a project file can not be found.
    """
    pass


class ProjectsDirectoryNotFoundError(SublpException, IOError):
    """
    Raised by sublp when a project directory can not be found.
    """
    pass


class UnmatchedInputString(SublpException, ValueError):
    """
    Rasied when input string cannot be successfully matched against
    any of the cases known by the dispatcher.
    """
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

    # def __init__(self, *args, **kwargs):
    #     cls = type(self)
    #     super(cls, self).__init__(*args, **kwargs)
    #     #assert(isinstance(self, cls))

    # @classmethod
    # def meets(cls, instance):
    #     if isinstance(instance, basestring):
    #         if os.path.isdir(instance):
    #             return True
    #     return False

    @classmethod
    def __instancecheck__(cls, instance):
        if isinstance(instance, basestring):
            if os.path.isdir(instance):
                return True
        return False

class ExistingFile(str):
    __metaclass__ = ValueMeta

    @classmethod
    def __instancecheck__(cls, instance):
        if isinstance(instance, basestring):
            if os.path.isfile(instance):
                return True
        if isinstance(instance, file):
            name = getattr(instance, 'name', '')
            if os.path.isfile(name):
                return True
        return False

ExistingPath = (ExistingDirectory, ExistingFile)

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
