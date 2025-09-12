from make_calls import return_main
from operators.mathematics import return_math, add

def test_return_main():
    assert return_main() == "main"

def test_return_math():
    assert return_math() == "math"

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0