# -*- coding: utf-8 -*-

"""Module containing the main functionality of the application."""

from .main import *  # import all public objects from main module

# Alternatively, you can import only specific objects:
# from .main import function1, function2, ClassName

# If the main module is just for entry points or setup, you can create a new
# module (e.g., `__init__.py`) and move the relevant code there.

# Example of moving the main function to `__init__.py`:

# from . import function1, function2, ClassName

# def main():
#     function1()
#     function2()
#     obj = ClassName()
#     obj.method()

# if __name__ == "__main__":
#     main()
