"""
Contains the dispatcher function - to be called by .sh
command-line scripts.
"""

import os
import subprocess
import sys

import dispatch_cases
import support
import errors
import interfaces
import configuration

__all__ = [
    'Sublp'
]

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

    cases = [
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
            if case.matches(_string):
                return case

        if hasattr(cls, 'fallback'):
            if cls.fallback.matches(_string):
                return cls.fallback

        raise errors.UnmatchedInputString(str.format(
            "Cannot find an appropriate sublime project file for '{0}'.",
            _string
        ))

    @classmethod
    def invoke(cls, case, _string):
        """
        @type: case: OpenProjectCaseInterface
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


if __name__ == "__main__":
    Sublp(sys.argv[1])
