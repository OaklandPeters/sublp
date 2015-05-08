"""
This is cool and useful

... but is getting heavily sidetracked for sublp


If/when this is working:
- Should register list of commands (property) based on decorator on methods
- Auto create commandline arguments
"""
from collections import Mapping


def register_command(*parse_args, **options):
    """Register a method as a commandline command.

    options:
        help=


    """
    def wrapper(function):
        function._is_command = True
        return function
    return wrapper


def get_commands(cls):
    return {
        (name, value)
        for name, value in vars(cls).items()
        if getattr(value, '_iscommand', False)
    }


def _combine(mappings):
    """Combine mappings. Doesn't account for nested behavior"""
    return {k: v for d in mappings for k, v in d.items()}

def _get_property(klass, name, self, default):
    if hasattr(klass, name):
        return getattr(klass, name).__get__(klass, self)
    else:
        return default




class HasCommands(object):
    """
    Mixin for command-bearing function
    """
    def __new__(cls, *args, **kwargs):
        cls._commands = get_commands(cls)
        self = super(HasCommands, cls).__new__(cls, *args, **kwargs)
        return self

    @property
    def commands(self):
        return self._commands

    @property
    def parser(self):
        return _combine(
            _get_property(parent, 'parser', self, dict())
            for parent in reversed(type(self).__bases__)
        )

    @parser.setter
    def parser(self, value):
        assert isinstance(value, Mapping)
        self._parser = value

    _parser = {}


class SublpType(HasCommands):
    """
    ~ Organizes callable commands.
    ... I could reorganize these as pure functions.
    """

    @register_command
    def list(self):
        pass

    @register_command
    def open(self, name):
        pass

    @register_command
    def delete(self, name):
        pass

    @register_command
    def create(self, name, path):
        pass



class GrandParent(HasCommands):
    _parser = {
        'help': 'john'
    }
