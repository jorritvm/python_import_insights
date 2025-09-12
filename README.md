# Python import insights

## Purpose
The purpose of this repo is to establish an ideal python project repository setup that covers the following desiderata:
- Execution works from command line, vs code, pycharm
- No tweaks to sys.path or PYTHONPATH are required
- A src-layout is used, with no code at the project root level
- Config files can be stored at the project root or in a config/ folder
- The pycharm IDE can resolve the imports correctly during code analysis
- Pytest works and can use imports relative to src/
- A virtual environment can be created at the project root level

To fully grasp the implications of the various setups, we need to understand how python imports work at a deeper level.
- Understand the difference between cwd and sys.path
- Understand how script vs module execution differ
- Understand absolute vs relative imports
- Understand the differences between modules, files, packages and folders


## Basics
CWD is the current working directory, i.e. the directory from which you started the python interpreter or script.
It can be obtained using `os.getcwd()`. It is important for python when resolving relative file paths. It has no direct relation to imports.

A python module is a file containing python code. It can be imported using the `import` statement. 
It can also be executed as a script.
A python package is different from a folder in that it contains an `__init__.py` file. 
Since python 3.3 this file is not strictly necessary anymore, but it can be used by the developer to control what is exported when the package is imported. 
A package can contain modules and sub-packages.

Python can execute code in two ways: as a script or as a module. 
When executing as a module, the module's name is set to the module's name.
When executing as a script, the module's name is set to `__main__`.
Hence, when running a module as a script, it will only execute code in the `__if __name__ == '__main__':`_ block.

`sys.path` is a list of strings that specifies the search path for modules. 
When you call `import` in the Python interpreter searches through a set of directories for the name provided. 
The list of directories that it searches is stored in `sys.path`.  
It is populated as follows:
1. The directory containing the script being run (or the current directory if in interactive mode), note that this means:
  - **When running a module as a script the module's path is added to `sys.path`.**
  - **When running a module as a module, the current working directory is added to `sys.path`.**
2. Standard library paths 
3. Site-packages (third-party packages)
4. Any paths specified in the PYTHONPATH environment variable

Virtual environment work because they modify entries 2 and 3 of the `sys.path`.

## The pitfall
To keep structure in your project, you want to avoid separate data, configuration and source code files. 
There are good reasons to avoid having source code at the project root level.
Once you make that decision, chances are your code only works in pycharm, but not from the command line or vs code.
Or the code works but your relative file imports now fail.

The internet is filled with people suggesting to modify `sys.path` in your code or to modify the PYTHONPATH environment variable.
This is a bad idea because it makes your code less portable, as it will only work in your specific setup.

## Setup 
* The pycharm project (.idea/) is created at the project root level
* A module `main.py` is available at root level, containing executable code and a function
* A subfolder src exists with module `main2.py`, containing only executable code

## Learnings
### pycharm injects the root folder and plugins folder into the sys.path
When we run `main.py` from the terminal we get:
```
PS C:\Users\jorrit\Desktop\pycharm_idea_at_root> py .\main.py
--- cwd ---
C:\Users\jorrit\Desktop\pycharm_idea_at_root
--- path ---
C:\Users\jorrit\Desktop\pycharm_idea_at_root 
C:\python\309\python39.zip
C:\python\309\DLLs
C:\python\309\lib
C:\python\309
```
Compare this to running `main.py` from pycharm using the green arrow:
```
C:\python\309\python.exe C:\Users\jorrit\Desktop\pycharm_idea_at_root\main.py 
--- cwd ---
C:\Users\jorrit\Desktop\pycharm_idea_at_root
--- path ---
C:\Users\jorrit\Desktop\pycharm_idea_at_root 
C:\Users\jorrit\Desktop\pycharm_idea_at_root                                       <-- injected by pycharm!
C:\Program Files\JetBrains\PyCharm 2023.1\plugins\python\helpers\pycharm_display   <-- injected by pycharm!
C:\python\309\python39.zip
C:\python\309\DLLs
```

### this means some code works in pycharm but not elsewhere!
`main2.py` has an import from module main
```
if __name__ == '__main__':
    import os
    print("--- cwd ---")
    print(os.getcwd())

    import sys
    print("--- path ---")
    for p in sys.path[:5]:
        print(p)

    from main import print_hi
    print_hi()
```
when we run it from the terminal it fails
```
PS C:\Users\jorrit\Desktop\pycharm_idea_at_root\src> py .\main2.py
--- cwd ---
C:\Users\jorrit\Desktop\pycharm_idea_at_root\src
--- path ---
C:\Users\jorrit\Desktop\pycharm_idea_at_root\src
C:\python\309\python39.zip
C:\python\309\DLLs
C:\python\309\lib
C:\python\309
Traceback (most recent call last):
  File "C:\Users\jorrit\Desktop\pycharm_idea_at_root\src\main2.py", line 12, in <module>
    from main import print_hi
ModuleNotFoundError: No module named 'main'
```
even running it from the root folder (different cwd) does not make a difference 
as not the CWD but the python source file path is added to `sys.path`!!!
```
PS C:\Users\jorrit\Desktop\pycharm_idea_at_root> py .\src\main2.py
--- cwd ---
C:\Users\jorrit\Desktop\pycharm_idea_at_root
--- path ---
C:\Users\jorrit\Desktop\pycharm_idea_at_root\src
C:\python\309\python39.zip
C:\python\309\DLLs
C:\python\309\lib
C:\python\309
Traceback (most recent call last):
  File "C:\Users\jorrit\Desktop\pycharm_idea_at_root\src\main2.py", line 12, in <module>
    from main import print_hi
ModuleNotFoundError: No module named 'main'
```
But if we run it from pycharm, there is no issue whatsoever, due to the injected root folder
```
C:\python\309\python.exe C:\Users\jorrit\Desktop\pycharm_idea_at_root\src\main2.py 
--- cwd ---
C:\Users\jorrit\Desktop\pycharm_idea_at_root\src
--- path ---
C:\Users\jorrit\Desktop\pycharm_idea_at_root\src
C:\Users\jorrit\Desktop\pycharm_idea_at_root
C:\Program Files\JetBrains\PyCharm 2023.1\plugins\python\helpers\pycharm_display
C:\python\309\python39.zip
C:\python\309\DLLs
Hi

Process finished with exit code 0
```

### mark directory as 'source root' makes things even worse (from a reproducibility POV)
Using this pycharm feature will add the marked folder to the `sys.path` in addition to the project root. 
Source: https://stackoverflow.com/questions/57360738/what-does-mark-directory-as-sources-root-really-do

### Ideal setup
- you should create your .idea project at project root level
- you should create your venv at project root level and store your requirements.txt there as well
- you should create your main source file in src/
  - src/ will be on sys.path 
  - all imports can be relative to src/ 
- you should mark your src/ folder in pycharm as "sources root"
  - this way it will appear in sys.path of your interactive console
  - you might need to restart your console
  - this allows you to send python code to your console (alt+shift+e) without lookup errors
  