Code Refactoring
-----------------
- Simplify the logic behind dispatcher_cases. Goal: input is two pieces of information: (1) folder/path, (2) project name. Usually one or the other is inferred.
    - Canonical form: sublp --name NEW_PROJECT_NAME --path RELATIVE_PATH
    - Lookup Project form: sublp EXISTING_PROJECT
    - Existing path form: sublp PATH --> translates to absolute path, and 
    - TL;DR: Places all project files in standard directory. Remove case where it looks for a project file inside a given directory. When given path to a folder, it looks for a project with the same name as the topmost folder.
- Edge-case: `sublp .` -> translate relative path to absolute path, and then get the folder name.
- Allow sublp to passthrough other arguments. EG 'sublp {name} path' should be equivalent to sublime --project=name path.
- Change configuration file to being a JSON file (sublprc.json), and add configuration reader function
- Create a version (sublp_dist) which combines everything in one file.


Project Support
------------------
- requirements.txt (pip freeze?)
- Test installation into virtualenv
    - Walk through installation process esp .bash_profile
- Fill in README
    - Examples of use
    - Purpose (as if speaking to office mate)
    - Windows compatible?
    - Note on Python2/3 compatibility
- Ask for help testing (Jason?)
