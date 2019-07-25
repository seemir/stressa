# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.domain.person import Person


class Male(Person):
    """
    Male class, i.e. first of only two gender classes

    """

    def __init__(self, age=0, income=0, kinder_garden='0', sfo='0'):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        age             : int, float, str
                          age of person
        income          : int, float
                          gross yearly income
        kinder_garden   : str
                          kids in kinder garden, true or false
        sfo             : str
                          After school programme, true or false

        """
        super().__init__(sex='m', age=age, income=income, kinder_garden=kinder_garden, sfo=sfo)

        self.age = self.set_age(age)
        self.kinder_garden = kinder_garden
        self.sfo = sfo
        self.income = str(income)
