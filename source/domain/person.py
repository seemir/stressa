# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from bisect import bisect_left


class Person:
    """
    Superclass for which all person domain objects are subclassed.

    """

    @staticmethod
    def set_age(age):
        """
        Converts age int to SIFO compatible str

        Parameters
        ----------
        age     : str
                  age to be converted

        Returns
        -------
        Out     : str
                  SIFO compatible age str
        """
        age_str = [0.41, 0.91, 1, 2, 3, 5, 9, 13, 17, 19, 50, 60, 66, 75]
        return str(age_str[bisect_left(age_str, age)])

    @staticmethod
    def evaluate_data_type(arg_dict):
        """
        Method that evaluates the type of objects in dictionary of {objects: types}. Raises
        TypeError if not match.

        Parameters
        ----------
        arg_dict    : dictionary
                      dict of arg: type to be evaluated
        """
        for arg, t in arg_dict.items():
            if not isinstance(arg, t):
                raise TypeError(
                    "expected type '{}', got '{}' instead".format(t.__name__, type(arg).__name__))

    def __init__(self, sex='m', age=0, income=0, kinder_garden=False, sfo=False):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        sex             : str
                          sex of the person, male ('m') or female ('f')
        age             : int, float, str
                          age of person
        income          : int, float
                          gross yearly income
        kinder_garden   : str
                          kids in kinder garden, true or false
        sfo             : str
                          After school programme, true or false

        """

        self.evaluate_data_type(
            {sex: str, age: (float, int), kinder_garden: str, sfo: str, income: (int, float)})

        self.sex = sex
        self.age = self.set_age(age)
        self.kinder_garden = '1' if kinder_garden else '0'
        self.sfo = sfo if sfo else '0'
        self.income = str(income)
