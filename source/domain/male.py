# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.log import logger
from .person import Person


class Male(Person):
    """
    Male class, i.e. first of only two gender classes

    """

    def __init__(self, age: (int, float, str) = 0, kinder_garden: str = '0', sfo: str = '0'):
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
        super().__init__('m', age, kinder_garden, sfo)
        logger.success(
            "created '{}', with id: [{}]".format(self.__class__.__name__, self.id))
