"""
Interfaces used for the dispatching cases, and for value-type-checking.
"""
import sys

__all__ = [
    'ExistingDirectory',
    'ExistingPath',
    'ExistingFile',
    'OpenProjectCaseInterface'
]

if sys.version_info[0] < 3:
    from .py2 import (ExistingDirectory, ExistingFile, ExistingPath, OpenProjectCaseInterface)  # pylint:disable=W0403
else:
    from .py3 import (ExistingDirectory, ExistingFile, ExistingPath, OpenProjectCaseInterface)  # pylint:disable=F0401
