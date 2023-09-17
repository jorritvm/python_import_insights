# Learn python/pycharm import quirks

## Purpose
This repo is to learn about the python import system and the impact a pycharm project has on that system.

## Basics
When running a script from the command line, the first item in `sys.path` will be the path to the script. 
The docs say that sys.path is then “initialized from the environment variable PYTHONPATH.

When you call `import` in the Python interpreter searches through a set of directories for the name provided. 
The list of directories that it searches is stored in `sys.path`.

`sys.path` can be modified during run-time. 
To modify the paths before starting Python, you can modify the PYTHONPATH environment variable.
You should never do this!

When we set up a virtual environment it injects itself in `sys.path`.

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