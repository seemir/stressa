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
                        "expected type 'Union[{}]', got '{}' instead".format(
                            ", ".join(dt.__name__ for dt in dtype), arg.__class__.__name__))

    @staticmethod
    def assert_arguments(obj_list: list, possible_list: list):
        """
        Method that evaluates the object in list to see if object are in set of possible values.
        Raises ValueError if not match.

        Parameters
        ----------
        obj_list       : list
                         list of object to be evaluated
        possible_list  : list of tuple


        """
        for i, obj in enumerate(obj_list):
            possible = possible_list[i]
            for name, value in possible.items():
                if obj and obj not in value:
                    raise ValueError(
                        "only possible values for '{}' are {}".format(name, value))

    @staticmethod
    def assert_non_negative(numbers, msg=""):
        """
        Evaluate a non-negative numeric (int, float). Raise ValueError if negative

        Parameters
        ----------
        numbers : list, str, int, float
                  number(s) to be evaluated
        msg     : str
                  message to display

        """
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
