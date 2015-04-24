NEW Simple Version
======================
Simplification: ALL project files stored in standard directory. First step on starting funciton - confirm/create the standard directory.

3 core functions:
    sublp (list|open|create)

Convenience polymorphism:
    sublp: → sublp list
    sublp $name: → sublp open $name
    sublp $name $path: → sublp create $name $path


Code Refactoring
-----------------
- Add additional commandline options:
    - Delete project: sublp -d {PROJECT-NAME}; -d, --delete
    - Create project: sublp -c {NAME} {PATH}; -c, --create
    - Query if project exists: sublp -e {NAME}; -e, --exists
    - Open project by name, if exists: sublp -n {NAME}; -n, --name
    - Open project by directory, infers name: subp -p {PATH}; -p, --path
- Add in auto-complete support, drawing {NAME} from standard projects directory
- Simplify the logic behind dispatcher_cases.
    - TL;DR: Remove cases:
        - Where it looks for a project file inside specified directory
        - Where you specify a project file by path
        - Project file will always be located in standard project directory
    - Cases:
        Canonical:
        sublp {NAME} {PATH}
            :: Canonical
            --> if already exists, errors
            --> if not exists, creates a project of NAME with open directory being PATH
        sublp {NAME}
            :: By-Name :: most common use-case
            --> sublp --name={NAME} --path={relative_path(NAME)}
            --> sublp {NAME} {PATH=relative_path(NAME)}
            --> sublp --name {NAME}
        sublp {PATH-TO-DIR}
            :: By-Dir :: commonly used to create new project
            --> sublp --name={top_directory(PATH-TO-DIR)} --path={PATH-TO-DIR}
            --> sublp {top_directory{PATH-TO-DIR}} {PATH={PATH-TO-DIR}}
            --> sublp --path {PATH}
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
