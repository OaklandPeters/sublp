"""
Exceptions
"""

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
