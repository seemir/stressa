# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.exception import InstantiationError
from source.log import main_logger
from source.util import Assertor
from bisect import bisect_left
from .entity import Entity


class Person(Entity):
    """
    Superclass for which all person domain classes are subclassed.

    """

    @staticmethod
    def _sifo_age(age: (int, float, str)):
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
        try:
            age = float(age)
        except Exception as e:
            raise TypeError("invalid numeric str, got '{}'".format(e))
        Assertor.assert_non_negative([age])

        sifo_yrs = [0.42, 0.92, 1, 2, 3, 5, 9, 13, 17, 19, 50, 60, 66, 75]
        return str(sifo_yrs[bisect_left(sifo_yrs, age)]) if age <= 75 else str(75)

    def __init__(self, sex: str = 'm', age: (int, float, str) = 0, kinder_garden: str = '0',
                 sfo: str = '0'):
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
        super().__init__()
        try:
            if type(self) == Person:
                raise InstantiationError(
                    "base class '{}' cannot be instantiated".format(self.__class__.__name__))

            Assertor.assert_data_type(
                {sex: str, age: (int, float, str), kinder_garden: str, sfo: str})

            Assertor.assert_arguments({kinder_garden: ['kinder_garden:', ('0', '1')],
                                       sfo: ['sfo:', ('0', '1', '2')]})

            if self._sifo_age(age) not in ('1', '2', '3', '5') and kinder_garden == '1':
                raise ValueError("only persons between 1-5 years can attend kinder_garden")

            if self._sifo_age(age) not in ('9', '13') and sfo == '1':
                raise ValueError("only persons between 6-13 years can attend sfo")

        except Exception as exp:
            main_logger.exception(exp)
            raise exp

        self._kjonn = sex
        self._alder = self._sifo_age(age)
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
    def alder(self, age: (int, float, str)):
        """
        age setter

        Parameters
        ----------
        age     : int, float, str
                  new age to be set

        """
        Assertor.assert_data_type({age: (float, int, str)})
        self._alder = self._sifo_age(age)

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
    def barnehage(self, kinder_garden: str):
        """
        kinder_garden status setter

        Parameters
        ----------
        kinder_garden   : str
                          new kinder_garden str

        """
        Assertor.assert_data_type({kinder_garden: str})
        Assertor.assert_arguments({kinder_garden: ['kinder_garden:', ('0', '1')]})
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
    def sfo(self, s: str):
        """
        after-school/sfo program setter

        Parameters
        ----------
        s       : str
                  new after-school/sfo str

        """
        Assertor.assert_data_type({s: str})
        Assertor.assert_arguments({s: ['kinder_garden:', ('0', '1')]})
        self._sfo = s
