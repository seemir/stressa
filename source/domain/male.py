# -*- coding: utf-8 -*-

"""
Male entity class implementation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from typing import Union

from source.util import LOGGER

from .person import Person


class Male(Person):
    """
    Male class, i.e. first of only two gender classes

    """

    def __init__(self, age: Union[int, float, str] = 0, kinder_garden: str = '0', sfo: str = '0'):
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

        """
        try:
            super().__init__('m', age, kinder_garden, sfo)
            LOGGER.success(
                "created '{}', with id: [{}]".format(self.__class__.__name__, self.id))
        except Exception as male_exception:
            LOGGER.exception(male_exception)
            raise male_exception
