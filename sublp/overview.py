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









