sublp
============


Synopsis
---------
Convenience Bash command-line function for opening SublimeText projects.
Very similar to `subl {PATH}` command, except looks for a
`{PATH}.sublime-project` file in several standard locations. If not found,
then it falls back to the behavior of `subl`.

Usage
---------
.. code::

    sublp {PROJECT-FILE-PATH}
    sublp {DIRECTORY-WITH-PROJECT-FILE}

Examples
----------
{{Specific examples from test files should go here}}


Installing
-----------
! setup does not work yet
Setup this package as regular::

    pip install sublp

Then, add to your .bash_profile::

    alias sublp='python /path/to/project/sublp.py'


Project File Locations
-----------------------
Runs one of four cases, based on the single argument to `sublp {1}`:

(1) Looks for a project file named by the argument.
(2) Looks for a project file, inside a directory named by the argument.
(3) Looks for a file of that name in the "standard" projects directory.
(4) If none of the above

Standard Projects Directory
----------------------------
By default this is: "~/Library/Application Support/Sublime Text 3/Packages/User/Projects". Currently this has to be specified inside sublp.py - but in the future
this will be able to be specified in some configuration file.

Tests
------
test_sublp.py runs Python unittests on the invernal/private Python functions.
test_invoke.py is intended to be ran 'manually' by commandline to test for '.invoke' commands which actually open SublimeText windows.

To run all unit-tests from commandline, use::
    cd sublp         # the outermost project directory
    python -m sublp.test_sublp         # standard unittests
    python -m sublp.test_invoke
    # OR, in Python 2.7+
    python -m unittest discover .      # standard unittests


Contributors
------------
Oakland John Peters.

License
-----------
Copyright MIT 2014.
