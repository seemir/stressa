# -*- coding: utf-8 -*-

"""
Utility class that acts like a static-type checker of python objects

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from abc import ABC, abstractmethod


class Assertor(ABC):
    """
    Class for asserting Python objects

    """

    @staticmethod
    def assert_data_types(arg_list: list, dtype_list: list):
        """
        Method that evaluates the type of objects in 'arg_list' against 'dtype_list'. Raises
        TypeError if not match.

        Parameters
        ----------
        arg_list    : list
                      arguments to be evaluated
        dtype_list  : list
                      types of corresponding arguments

        """
        for i, arg in enumerate(arg_list):
            dtype = dtype_list[i]
            if not isinstance(arg, dtype):
                try:
                    raise TypeError(
                        "expected type '{}', got '{}' instead".format(dtype.__name__,
                                                                      arg.__class__.__name__))
                except AttributeError:
                    raise TypeError(
                        "expected type '{}', got '{}' instead".format(
                            " or ".join(dt.__name__ for dt in dtype), arg.__class__.__name__))

    @staticmethod
    def assert_arguments(arg_dict: dict):
        """
        Method that evaluates the object in dictionary of {object: [name, possible]} to see if
        object is in possibility. Raises ValueError if not match.

        Parameters
        ----------
        arg_dict    : dictionary
                      dict of {object: [name, possible]} to be evaluated

        """
        for arg, arg_list in arg_dict.items():
            name, possible = arg_list[0], arg_list[1]
            if arg not in possible:
                raise ValueError(
                    "only possible values for '{}' are {}".format(name, possible))

    @staticmethod
    def assert_non_negative(numbers):
        """
        Evaluate a non-negative numeric (int, float). Raise ValueError if negative

        Parameters
        ----------
        numbers : list, str, int, float
                  number(s) to be evaluated

        """
        msg = "only non-negative numbers accepted"
        if isinstance(numbers, list):
            for number in numbers:
                if float(number) < 0:
                    raise ValueError(msg)
        else:
            if float(numbers) < 0:
                raise ValueError(msg)

    @abstractmethod
    def __init__(self):
        """
        Abstract class, so class cannot be instantiated

        """
