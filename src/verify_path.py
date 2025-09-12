import os
import sys
from pprint import pprint

if __name__ == '__main__':
    print("--- cwd ---")
    print(os.getcwd())

    print("--- path ---")
    pprint(sys.path[:5])
