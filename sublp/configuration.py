"""
Specifies user-specific parameters.
"""
import os

__all__ =[
    'PROJECTS_DIRECTORY',
    'DEFAULT_TO_PROJECTS_DIRECTORY'
]

PROJECTS_DIRECTORY = (
    "/Users/opeters/Library/Application Support/"
    "Sublime Text 3/Packages/User/Projects"
)

# If True, then fallback which creates projects file,
#   will place it in PROJECTS_DIRECTORY
DEFAULT_TO_PROJECTS_DIRECTORY = True

if PROJECTS_DIRECTORY is not None:
    if not os.path.isdir(PROJECTS_DIRECTORY):
        os.mkdir(PROJECTS_DIRECTORY)
