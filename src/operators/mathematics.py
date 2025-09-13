from utils.simple_logger import log

def return_math():
    return "math"

def add(a, b):
    log(f"adding {a} + {b}")
    return a + b

if __name__ == '__main__':
    import os
    import sys
    print("cwd: " + os.getcwd())
    print("sys.path[0]: " + sys.path[0])
    add(1, 1)
