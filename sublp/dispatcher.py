"""
Contains the dispatcher function - to be called by .sh
command-line scripts.
"""
import subprocess
import sys
import warnings

from . import dispatch_cases
from . import support
from . import errors
from . import interfaces
from . import configuration

__all__ = [
    'Sublp'
]


class ClassProperty(object):
    """Creates read-only class-level property."""
    def __init__(self, function):
        self.function = function
    def __get__(self, obj, owner):
        return self.function(owner)


class Sublp(object):
    """
    Generic-function/dispatcher-function for sublp commandline function.
    """
    # Instance case objects
    OpenProjectFromFilePath = dispatch_cases.OpenProjectFromFilePath()
    OpenProjectFromDirectory = dispatch_cases.OpenProjectFromDirectory()
    OpenProjectFromName = dispatch_cases.OpenProjectFromName(
        projects_directory=configuration.PROJECTS_DIRECTORY
    )
    OpenProjectFallback = dispatch_cases.OpenProjectFallback()

    _cases = [  # accessed via 'cases' ClassProperty
        OpenProjectFromFilePath,
        OpenProjectFromDirectory,
        OpenProjectFromName
    ]
    fallback = OpenProjectFallback

    def __new__(cls, _string):
        return cls.__call__(_string)

    @classmethod
    def __call__(cls, _string):
        """
        Primary flow-control.
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
        @rtype: OpenProjectCaseInterface
        """

        _string = cls._validate_string(_string)
        for case in cls.cases:
            try:  # errors in a case --> skip over that case
                if case.matches(_string):
                    return case
            except errors.SublpException as exc:
                cls._case_warning(case, exc)

        raise errors.UnmatchedInputString(str.format(
            "Cannot find an appropriate sublime project file for '{0}'.",
            _string
        ))

    @classmethod
    def invoke(cls, case, _string):
        """
        @type: case: interfaces.OpenProjectCaseInterface
        @type: _string: str
        @rtype: None
        """

        _string = cls._validate_string(_string)
        command = case.command(_string)
        subprocess.call(command, shell=True)

    @classmethod
    def _validate_string(cls, _string):
        """
        Validate input string.
        @type: _string: str
        @rtype: str
        """

        if not isinstance(_string, str):
            raise TypeError("'_string' must be instance of str.")
        return _string

    @classmethod
    def _case_warning(cls, case, exception):
        """
        @type: case: interfaces.OpenProjectCaseInterface
        @type: exception: Exception
        """
        warnings.warn(str.format(
            "WARNING: Exception in case '{name}', skipping:\n{message}",
            name=type(case).__name__, message=str(exception)
        ))

    @ClassProperty
    def cases(cls):  # pylint:disable=E0213
        """
        Yields the cases, appending the fallback case if one is present.
        Iterator. Read-only property.
        """

        for case in cls._cases:
            yield case
        if hasattr(cls, 'fallback'):
            if cls.fallback is not None:
                yield cls.fallback

# if __name__ == "__main__":
#     Sublp(sys.argv[1])
