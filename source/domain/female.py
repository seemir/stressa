# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.domain.person import Person
from source.util.assertor import Assertor


class Female(Person):
    """
    Female class, i.e. second of only two gender classes

    """

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
        pregnant     : float, int, str
                       new pregnancy str to be set

        """
        Assertor.assert_date_type({pregnant: str})
        Assertor.assert_arguments({pregnant: ['pregnant', ('0', '1')]})
        Assertor.assert_two_boolean(self.alder not in ('19', '50'), pregnant == '1',
                                       "pregnancy at this age is not possible")
        self._gravid = pregnant
