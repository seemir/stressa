# -*- coding: utf-8 -*-

"""
Person entity base class implementation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from typing import Union
from bisect import bisect_left

from source.util import Assertor, Tracking

from .entity import Entity


class Person(Entity):
    """
    Superclass for which all person domain classes are subclassed.

    """

    @Tracking
    def sifo_age(self, age: Union[int, float, str]):
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
        except Exception as exp:
            raise TypeError(f"invalid numeric str, got '{exp}'")

        Assertor.assert_non_negative([age])
        sifo_yrs = [0.41, 0.91, 1, 2, 3, 5, 9, 13, 17, 19, 30, 50, 60, 66, 74, 999]
        return str(sifo_yrs[bisect_left(sifo_yrs, age)]) if age <= 999 else str(999)

    def __init__(self, sex: str = 'm', age: Union[int, float, str] = 0, kinder_garden: str = '0',
                 sfo: str = '0', student: str = '0'):
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

        Assertor.assert_data_types([sex, age, kinder_garden, sfo],
                                   [str, (int, float, str), str, str])
        Assertor.assert_arguments([kinder_garden, sfo],
                                  [{"kinder_garden": ('0', '1')}, {"sfo": ('0', '1', '2')}])

        if self.sifo_age(age) not in ('1', '2', '3', '5') and kinder_garden == '1':
            raise ValueError("only persons between 1-5 years can attend kinder_garden")

        if self.sifo_age(age) not in ('9', '13') and sfo == '1':
            raise ValueError("only persons between 6-13 years can attend sfo")

        if self.sifo_age(age) != '30' and student == '1':
            raise ValueError("only persons between 20-30 years can be students")

        self._kjonn = sex
        self._alder = self.sifo_age(age)
        self._barnehage = kinder_garden
        self._sfo = sfo
        self._student = student

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
    def alder(self, age: Union[int, float, str]):
        """
        age setter

        Parameters
        ----------
        age     : int, float, str
                  new age to be set

        """
        Assertor.assert_data_types([age], [(float, int, str)])
        self._alder = self.sifo_age(age)

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
        Assertor.assert_data_types([kinder_garden], [str])
        Assertor.assert_arguments([kinder_garden], [{"kinder_garden": ('0', '1')}])
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
    def sfo(self, _sfo: str):
        """
        after-school/sfo program setter

        Parameters
        ----------
        _sfo       : str
                     new after-school/sfo str

        """
        Assertor.assert_data_types([_sfo], [str])
        Assertor.assert_arguments([_sfo], [{"sfo": ('0', '1')}])
        self._sfo = _sfo

    @property
    def student(self):
        """
        student getter

        Returns
        -------
        out         : str
                      active student str in Person object

        """
        return self._student

    @student.setter
    def student(self, _student: str):
        """
        student setter

        Parameters
        ----------
        _student       : str
                         new student str

        """
        Assertor.assert_data_types([_student], [str])
        Assertor.assert_arguments([_student], [{"student": ('0', '1')}])
        self._student = _student
