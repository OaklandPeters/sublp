"""
Exceptions raised in the sublp package.
"""

__all__ = [
    'SublpException',
    'ProjectNotFoundError',
    'ProjectsDirectoryNotFoundError',
    'UnmatchedInputString'
]

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
