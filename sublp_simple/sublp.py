"""


@todo: Way to find user's Sublime Text directory
@todo: Record the directory the user called commandline from (os.curdir?)
@todo: Have config file hidden behind an object.
    Because... for now this is a commandline tool. In future, going to be a Sublime plugin
"""
import sys
import os
import collections


class SublpException(Exception):
    """Base exception type for project"""
    pass


class SublpParseError(SublpException, RuntimeError):
    """Error parsing commandline-arguments."""
    pass

class SublpCommandError(SublpException, ValueError):
    """When trying to get invalid options"""
    pass





class SublpType(HasCommands):
    """
    ~ Organizes callable commands.
    ... I could reorganize these as pure functions.
    """
       

    def __init__(self, *args, **kwargs):
        if kwargs.get('project_directory', False):
            self._project_directory = kwargs['project_directory']

    @property
    def project_directory(self):
        """Directory for user's `sublp` related .sublime-project."""
        return self._project_directory
    _project_directory = os.path.join("Sublime Text 3", "User")

    keywords = ("list", "open", "create", "delete")

    @property
    def commands(self):
        return {
            'list': self.list,
            'open': self.open,
            'create': self.create,
            'delete': self.delete
        }


    @register_command
    def list(self):
        """List projects in user's project directory."""
        print(str.format(
            "Listing project files in project directory `{pdir}`",
            pdir=self.project_directory
        ))

    def open(self, path):
        """Open a project in the user's project directory."""
        print(str.format(
            "Open project named '{path}'",
            path=path
        ))

    def create(self, name, path):
        """Create, then open, a project in the user's project directory.
        @todo: Consider whether path should be optional.
        """
        print(str.format(
            "Creating project for name '{name}' and path '{path}'.",
            name=name,
            path=path
        ))

    def delete(self, name):
        """Delete project from user's project directory."""
        print(str.format(
            "Delete project named '{name}'", name
        ))

Sublp = SublpType()  # user/config data should be passed in.


class SublpCommand(collections.Callable):
    def __new__(cls, name):
        try:
            return Sublp.commands[name]
        except KeyError as exc:
            raise Sublp



def parse_tokens(argv):
    """
    @todo: Change structure. step 1: check first for keywords, step 2: consider positional options
    """
    # this_file = argv[0]
    words = argv[1:]

    if len(words) == 0:
        first = None
    else:
        first = words[0]
    rest = words[1:]

    # sublp list
    # sublp
    # ------------
    if len(words) == 1 and first == "list":
        return Sublp.list()
    elif len(words) == 0:
        return Sublp.list()

    # sublp delete $name
    elif len(words) == 2 and first == "open":
        return Sublp.delete(*rest)

    # sublp open $name
    # sublp $name
    # ------------
    elif len(words) == 2 and first == "open":
        return Sublp.open(*rest)        # functools.partial(Sublp.list, *rest)
    elif len(words) == 1 and first not in Sublp.keywords:
        return Sublp.open(*rest)

    # sublp create $name $path
    # sublp $name $path
    # ------------
    elif len(words) == 3 and first == "create":
        return Sublp.create(*rest)
    elif len(words) == 2 and first not in Sublp.keywords:
        return Sublp.create(*rest)

    # Invalid input
    # ------------
    else:
        raise SublpParseError("Unrecognize input: "+str(words))


def main(argv):
    parse_tokens(argv)


if __name__ == "__main__":
    main(sys.argv)
