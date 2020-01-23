# -*- coding: utf-8 -*-

"""
Female entity class implementation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from typing import Union

from source.util import Assertor

from .person import Person


class Female(Person):
    """
    Female class, i.e. second of only two gender classes

    """

    def __init__(self, age: Union[int, float, str] = 0, kinder_garden: str = '0', sfo: str = '0',
                 pregnant: str = '0'):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        age             : int, float, str
                          age of person
        kinder_garden   : str
                          kids in kinder garden, '1' true or '0' false
        sfo             : str
                          After school programme, '1' true or '0' false
        pregnant        : str
                          Pregnant female, '1' true or '0' false

        """
        try:
            super().__init__('k', age, kinder_garden, sfo)
            Assertor.assert_data_types([age, kinder_garden, sfo], [(float, int, str), str, str])
            Assertor.assert_arguments([pregnant], [{"pregnant": ('0', '1')}])

            if Person.sifo_age(age) not in ('19', '50') and pregnant == '1':
                raise ValueError("pregnancy at this age is not possible")

            self._gravid = pregnant
        except Exception as female_exception:
            raise female_exception

    @property
    def gravid(self):
        """
        pregnancy status getter

        Returns
        -------
        Out     : str
                  pregnancy str

        """
        return self._gravid

    @gravid.setter
    def gravid(self, pregnant: str):
        """
        pregnancy setter

        Parameters
        ----------
        pregnant     : str
                       new pregnancy str to be set

        """
        Assertor.assert_data_types([pregnant], [str])
        Assertor.assert_arguments([pregnant], [{"pregnant": ('0', '1')}])
        self._gravid = pregnant
