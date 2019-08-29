# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'


class Evaluator:
    """
    Class for evaluating Python objects

    """

    @staticmethod
    def evaluate_data_type(dtype_dict):
        """
        Method that evaluates the type of objects in dictionary of {object: type}. Raises
        TypeError if not match.

        Parameters
        ----------
        dtype_dict    : dictionary
                        dict of object: type(s) to be evaluated

        """
        for obj, t in dtype_dict.items():
            if not isinstance(obj, t):
                raise TypeError(
                    "expected type '{}', got '{}' instead".format(t, type(obj).__name__))

    @staticmethod
    def evaluate_arguments(arg_dict):
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
    def evaluate_two_boolean(bool_1, bool_2, text):
        """
        Evaluate two boolean expressions with logical AND raise ValueError with text if False
        
        Parameters
        ----------
        bool_1    : bool
                    first boolean expression
        bool_2    : bool
                    second boolean expression
        text      : str
                    text to outputted in ValueError exception

        """
        if bool_1 and bool_2:
            raise ValueError(text)
