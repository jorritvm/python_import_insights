# Press the green button in the gutter to run the script.
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

    from sister import print_sister
    print_sister()
