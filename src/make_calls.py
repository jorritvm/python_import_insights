from operators.mathematics import add, return_math

def return_main():
    return "main"

if __name__ == '__main__':
    print(f"calling main: {return_main()}")
    print(f"calling math: {return_math()}")
    print(f"making a sum: {add(10,10)}")


