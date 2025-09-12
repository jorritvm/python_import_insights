def return_math():
    return "math"

def add(a, b):
    return a + b

if __name__ == '__main__':
    import os
    print("--- cwd ---")
    print(os.getcwd())

    import sys
    print("--- path ---")
    for p in sys.path[:5]:
        print(p)

    from src.main import print_hi
    print_hi()

    from utils import print_sister
    print_sister()
