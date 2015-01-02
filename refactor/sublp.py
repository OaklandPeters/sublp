"""
@todo: Copy docstring signature from OpenProjectCaseInterface into cases.
@todo: Add __call__ to cases - should open sublime appropriately

@todo: Write __all__ for each file

@todo: Make cases instancable
@todo: Make cases instanced inside Sublp class
@todo: Make OpenProjectFromName accept project directory as argument.
@todo: Change importation to proper relative imports (requires changing test_sublp.py first)
"""

import os
import subprocess
import sys

import dispatch_cases
import support
import errors
import interfaces
# if sys.version_info[0] < 3:
#     from py2 import (ExistingDirectory, ExistingPath, OpenProjectCaseInterface)  # pylint:disable=W0403
# else:
#     from py3 import (ExistingDirectory, ExistingPath, OpenProjectCaseInterface)  # pylint:disable=F0401





#===================================================
# Dispatcher
#===================================================
class Sublp(object):
    """
    Generic-function/dispatcher-function for sublp commandline function.
    """
    cases = [
        dispatch_cases.OpenProjectFromFilePath,
        dispatch_cases.OpenProjectFromDirectory,
        dispatch_cases.OpenProjectFromName,
        dispatch_cases.OpenProjectFallback
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
        @returns: OpenProjectCaseInterface
        """
        _string = cls._validate_string(_string)

        for case in cls.cases:
            if case.matches(_string):
                return case

        raise errors.UnmatchedInputString(str.format(
            "Cannot find an appropriate sublime project file for '{0}'.",
            _string
        ))

    @classmethod
    def invoke(cls, case, _string):
        """
        @type: case: OpenProjectCaseInterface
        @returns: None
        """
        _string = cls._validate_string(_string)
        command = case.command(_string)
        subprocess.call(command, shell=True)

    @classmethod
    def _validate_string(cls, _string):
        """Validate input string."""
        if not isinstance(_string, str):
            raise TypeError("'_string' must be instance of str.")
        return _string


#===================================================
# Exceptions
#===================================================



#===================================================
# Support Functions
#===================================================
