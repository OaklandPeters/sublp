

class SublimeProject(object):
    """
    ~ file manager
    create the file if it doesn't exist
    """
    def __init__(self, path, projects_directory=None):
        validate(path, str)

        if projects_directory is None:
            projects_directory = Sublp.projects_directory

        validate(projects_directory, str)
        validate(projects_directory, NonEmpty)

        validate(projects)

        if not project_exists(path):

        if not exists(path):

