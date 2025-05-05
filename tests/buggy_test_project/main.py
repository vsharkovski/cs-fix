from math_ops import divide


def main():
    for range in range(3):  # F402: import 'range' shadowed by loop variable
        print("Hello")

    result = divide(10)  # F706: wrong number of arguments (divide expects 2)
    print("Result:", result)

    print(undeclared_var)  # F821: undefined name


main()
