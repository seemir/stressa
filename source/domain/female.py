# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.domain.person import Person
from source.util.assertor import Assertor


class Female(Person):
    """
    Female class, i.e. second of only two gender classes

    """

    @staticmethod
    def assert_pregnancy(age, pregnant):
        """
        Assert that pregnant argument is str with only possible values '0' or '1' and that only
        females between 19-50 years can have pregnancy. TypeError is thrown if type is not str and
        ValueError otherwise.

        Parameters
        ----------
        age             : int, float, str
                          age of female
        pregnant        : str
                          pregnancy argument

        """
        Assertor.assert_date_type({age: (float, int, str), pregnant: str})
        Assertor.assert_arguments({pregnant: ['pregnant', ('0', '1')]})
        Assertor.assert_two_boolean(Person.set_age(age) not in ('19', '50'), pregnant == '1',
                                    "pregnancy at this age is not possible")

    def __init__(self, age=0, kinder_garden='0', sfo='0', pregnant='0'):
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
        super().__init__(sex='k', age=age, kinder_garden=kinder_garden, sfo=sfo)
        self.assert_pregnancy(age, pregnant)
        self._gravid = pregnant

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
    def gravid(self, pregnant):
        """
        pregnancy setter

        Parameters
        ----------
        pregnant     : str
                       new pregnancy str to be set

        """
        self.assert_pregnancy(self.alder, pregnant)
        self._gravid = pregnant
