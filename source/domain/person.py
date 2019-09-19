# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.exception.base_class_cannot_be_instantiated import BaseClassCannotBeInstantiated
from source.util.assertor import Assertor
from bisect import bisect_left


class Person:
    """
    Superclass for which all person domain classes are subclassed.

    """

    @staticmethod
    def set_age(age):
        """
        Converts age into SIFO compatible str

        Parameters
        ----------
        age     : int, float, str
                  age to be converted

        Returns
        -------
        Out     : str
                  SIFO compatible age str
        """
        Assertor.assert_date_type({age: (int, float, str)})
        try:
            age = float(age)
        except Exception as e:
            raise TypeError("invalid numeric str, got '{}'".format(e))
        Assertor.assert_non_negative(age)

        sifo_yrs = [0.42, 0.92, 1, 2, 3, 5, 9, 13, 17, 19, 50, 60, 66, 75]
        return str(sifo_yrs[bisect_left(sifo_yrs, age)]) if age <= 75 else str(75)

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
                          after school programme, '0' no, '1' half-day or '2' full-day

        """
        if type(self) == Person:
            raise BaseClassCannotBeInstantiated(
                "base class '{}' cannot be instantiated".format(self.__class__.__name__))

        Assertor.assert_date_type(
            {sex: str, age: (float, int, str), kinder_garden: str, sfo: str})

        Assertor.assert_arguments({sex: ['sex:', ('m', 'k')],
                                   kinder_garden: ['kinder_garden:', ('0', '1')],
                                   sfo: ['sfo:', ('0', '1')]})

        Assertor.assert_two_boolean(self.set_age(age) not in ('1', '2', '3', '5'),
                                    kinder_garden == '1',
                                       "only persons between 1-5 years can attend kinder_garden")

        Assertor.assert_two_boolean(self.set_age(age) not in ('9', '13'), sfo == '1',
                                       "only persons between 6-13 years can attend sfo")

        self._kjonn = sex
        self._alder = self.set_age(age)
        self._barnehage = kinder_garden
        self._sfo = sfo

    @property
    def kjonn(self):
        """
        gender/sex getter

        Returns
        -------
        Out     : str
                  gender/sex of the active Person object

        """
        return self._kjonn

    @property
    def alder(self):
        """
        age getter

        Returns
        -------
        Out     : str
                  SIFO compatible age str

        """
        return self._alder

    @alder.setter
    def alder(self, age):
        """
        age setter

        Parameters
        ----------
        age     : float, int, str
                  new age to be set

        """
        Assertor.assert_date_type({age: (float, int, str)})
        self._alder = self.set_age(age)

    @property
    def barnehage(self):
        """
        kinder_garden status getter

        Returns
        -------
        Out         : str
                      kids in kinder_garden, '1' true or '0' false

        """
        return self._barnehage

    @barnehage.setter
    def barnehage(self, kinder_garden):
        """
        kinder_garden status setter

        Parameters
        ----------
        kinder_garden   : str
                          new kinder_garden str

        """
        Assertor.assert_date_type({kinder_garden: str})
        Assertor.assert_arguments({kinder_garden: ['kinder_garden:', ('0', '1')]})
        Assertor.assert_two_boolean(self.set_age(self.alder) not in ('1', '2', '3', '5'),
                                    kinder_garden == '1',
                                       "only persons between 1-5 years can attend kinder_garden")
        self._barnehage = kinder_garden

    @property
    def sfo(self):
        """
        after-school/sfo program getter

        Returns
        -------
        out         : str
                      active after-school/sfo str in Person object

        """
        return self._sfo

    @sfo.setter
    def sfo(self, s):
        """
        after-school/sfo program setter

        Parameters
        ----------
        s       : str
                  new after-school/sfo str

        """
        Assertor.assert_date_type({s: str})
        Assertor.assert_arguments({s: ['sfo:', ('0', '1')]})
        Assertor.assert_two_boolean(self.set_age(self.alder) not in ('9', '13'), s == '1',
                                       "only persons between 6-13 years can attend sfo")
        self._sfo = s
