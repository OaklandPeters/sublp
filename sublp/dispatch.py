"""
Dispatcher
"""

from sublp import cases

class sublp(object):
    """
    Generic-function/dispatcher-function for sublp commandline function.
    """
    cases = [
        cases.OpenFromProjectFilePath,
        cases.OpenFromDirectory,
        cases.OpenFromProjectName,
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
        Invoke specific case with given arguments.
        @type: case: ProjectDispatchInterface
        @returns: None
        """
        command = case.form_command(_string)
        subprocess.call(command, shell=True)



class SublpDispatcher(object):
    """
    New draft of sublp dispatcher - this one uses instance-able
    case objects.
    """
    def __init__(self, projects_directory=None):



    def __new__(cls, _string, projects_directory=None):
        return cls.__call__(_string, projects_directory=projects_directory)

    def __call__(cls, _string, projects_directory=None):
        case = cls.match(_string)
        cls.invoke(case, _string)

    def get_cases(cls, projects_directory=None):
        cases = [
            cases.OpenFromProjectFilePath(),
            cases.OpenFromDirectory(),
            cases.OpenFromProjectName(projects_directory=projects_directory),
        ]

    @classmethod
    def match(cls, _string):
        """
        Finds case class which matches the input.
        @type: _string: str
        @returns: ProjectDispatchInterface
        """
        for case in cls.cases:
            if case.match
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

def sublp(_string, projects_directory=None):
    dispatcher = SublpDispatcher(projects_directory=projects_directory)
    return dispatcher(_string)
