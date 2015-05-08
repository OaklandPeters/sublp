"""

git style args
----------------
Using sub-commands (subparser)
    https://docs.python.org/2.7/library/argparse.html#sub-commands


add_argument
    name : name, -n, --name
    type : type to which to convert this
        int, file,
        (most builtins) - add a path type
    required
    help :
    metavar : name for argument in usage message
    dest : name of attribute to be added to return object


@todo: Create subparsers for each command (list|open|create|delete)
@todo: Combine with positional argument parsers

Advanced:
@todo: setdir - for setting the user's project directory
"""

import sublp
import argparse


parser = argparse.ArgumentParser(prog="sublp")
# parser.add_argument(
#     "--projdir", type=str, dest="project_directory"
# )
subparsers = parser.add_subparsers(help="List of commands: ", dest="command")
_list = subparsers.add_parser('list', help="List projects in user's project directory.")
_create = subparsers.add_parser('create',
    help="Create a new project file in user's project directory."
)
_create.add_argument('name', type=str, help="Name of .sublime-project")
_create.add_argument('path', type=str, help="Path to directory of project files.")
_open = subparsers.add_parser('open', help="Open an existing project.")
_open.add_argument('name', type=str, help="Name of .sublime-project")
_delete = subparsers.add_parser('delete')



def create(name, path):
    print("I see name: {0} and path: {1}".format(name, path))

def _callit(namespace, function):
    return function(**vars(namespace))

def main(argv):
    pass


if __name__ == "__main__":
    arguments = parser.parse_args()


    print()
    print("arguments:", type(arguments), arguments)
    print()
    import pdb
    pdb.set_trace()
    print()
