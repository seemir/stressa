# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.exception import BaseClassCannotBeInstantiated


class Assertor:
    """
    Class for asserting Python objects

    """

    @staticmethod
    def assert_date_type(dtype_dict: dict):
        """
        Method that evaluates the type of objects in dictionary of {object: type}. Raises
        TypeError if not match.

        Parameters
        ----------
        dtype_dict    : dict
                        dict of object: type(s) to be evaluated

        """
        for obj, t in dtype_dict.items():
            if not isinstance(obj, t):
                raise TypeError(
                    "expected type '{}', got '{}' instead".format(t, type(obj).__name__))

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
        for arg, ls in arg_dict.items():
            name, possible = ls[0], ls[1]
            if arg not in possible:
                raise ValueError(
                    "only possible values for '{}' are {}".format(name, possible))

    @staticmethod
    def assert_two_boolean(bool_a: bool, bool_2: bool, text: str):
        """
        Evaluate two boolean expressions with logical AND raise ValueError with text if False
        
        Parameters
        ----------
        bool_a    : bool
                    first boolean expression
        bool_2    : bool
                    second boolean expression
        text      : str
                    text to outputted in ValueError exception

        """
        if bool_a and bool_2:
            raise ValueError(text)

    @staticmethod
    def assert_non_negative(num):
        """
        Evaluate a non-negative numeric (int, float). Raise ValueError if negative

        Parameters
        ----------
        num     : int, float, str
                  number(s) to be evaluated

        """
        if not float(num) >= 0:
            raise ValueError("only non-negative numbers accepted, got '{}'".format(num))

    def __init__(self):
        """
        Abstract class, so class cannot be instantiated

        """
        if type(self) == Assertor:
            raise BaseClassCannotBeInstantiated(
                "base class '{}' cannot be instantiated".format(self.__class__.__name__))
