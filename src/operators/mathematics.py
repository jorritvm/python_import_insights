from utils.simple_logger import log


def return_math():
    return "math"


def add(a, b):
    log(f"adding {a} + {b}")
    return a + b


if __name__ == '__main__':
    import os

    print("--- cwd ---")
    print(os.getcwd())

    import sys

    print("--- path ---")
    for p in sys.path[:5]:
        print(p)

    add(1, 1)
