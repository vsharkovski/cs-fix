import os, sys


def compute_area(radius):
    pi = 3.14159
    area = pi * radius**2
    return area


def main():
    user_input = input("Enter radius: ")
    result = compute_area(float(user_input))
    print("Area is:", result)
    unused_var = 42

    if user_input == None:
        print("No input provided")

    try:
        val = int("123abc")
    except:
        print("An error occurred")


main()
