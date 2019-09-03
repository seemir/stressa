# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.exception.base_class_cannot_be_instantiated import BaseClassCannotBeInstantiated
from source.util.evaluator import Evaluator
from bisect import bisect_left


class Person:
    """
    Superclass for which all person domain objects are subclassed.

    """

    @staticmethod
    def set_age(age):
        """
        Converts age into SIFO compatible str

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
        return str(age_str[bisect_left(age_str, int(age))]) if int(age) <= 75 else 75

    def __init__(self, sex='m', age=0, kinder_garden='0', sfo='0'):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        sex             : str
                          sex of the person, male ('m') or female ('f')
        age             : int, float, str
                          age of person
        kinder_garden   : str
                          kids in kinder_garden, '1' true or '0' false
        sfo             : str
                          after school programme, '1' true or '0' false

        """
        if type(self) == Person:
            raise BaseClassCannotBeInstantiated(
                "base class '{}' cannot be instantiated".format(self.__class__.__name__))

        Evaluator.evaluate_data_type(
            {sex: str, age: (float, int, str), kinder_garden: str, sfo: str})

        Evaluator.evaluate_arguments({sex: ['sex:', ('m', 'k')],
                                      kinder_garden: ['kinder_garden:', ('0', '1')],
                                      sfo: ['sfo:', ('0', '1')]})

        Evaluator.evaluate_two_boolean(self.set_age(age) not in ('1', '2', '3', '5'),
                                       kinder_garden == '1',
                                       "only persons between 1-5 years can attend kinder_garden")

        Evaluator.evaluate_two_boolean(self.set_age(age) not in ('9', '13'), sfo == '1',
                                       "only persons between 6-13 years can attend sfo")

        self.kjonn = sex
        self.alder = self.set_age(age)
        self.barnehage = kinder_garden
        self.sfo = sfo

    def get_properties(self):
        """
        return all active properties and values in a dictionary

        Returns
        -------
        Out     : dict
                  dictionary of all active properties

        """
        return self.__dict__
