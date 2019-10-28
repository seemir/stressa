# -*- coding: utf-8 -*-

"""
Family entity class implementation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from typing import Union

from source.exception import DomainError
from source.util import Assertor
from source.log import LOGGER
from .entity import Entity
from .female import Female
from .male import Male


class Family(Entity):
    """
    Family entity class

    """

    @staticmethod
    def _assert_family_members(family_members: list):
        """
        Checking the family_members object. In this implementation a Family has the following
        characteristics:

        - Needs to be a list
        - Cannot be an empty list
        - All objects in the list must be either of class Male or Female
        - A family must have guardianship, i.e. have at least one person older than 17

        Parameters
        ----------
        family_members  : list
                          list of Male or Female objects

        """
        Assertor.assert_data_types([family_members], [list])

        if not family_members:
            raise ValueError("family_members cannot be empty, got '[]'")

        for family_member in family_members:
            Assertor.assert_data_types([family_member], [(Male, Female)])

        if all(int(family_member.alder) < 18 for family_member in family_members):
            raise DomainError("no guardianship found, i.e. family must have at least "
                              "one person older than 17 years.")

    def __init__(self, family_members: list = None, income: Union[int, float, str] = 0,
                 cars: Union[int, str] = 0):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        family_members  : list
                          list of Person (Male or Female) instances
        income          : int, float, str
                          gross yearly income
        cars            : int, str
                          number of cars in the family

        """
        super().__init__()
        try:
            self._assert_family_members(family_members)
            Assertor.assert_data_types([income, cars], [(int, float, str), (int, str)])
            Assertor.assert_non_negative([income, cars])

            self._family_members = family_members
            self._inntekt = str(income)
            self._antall_biler = str(cars)
            LOGGER.success(
                "created '{}', with id: [{}]".format(self.__class__.__name__, self.id_str))
        except Exception as family_exception:
            LOGGER.exception(family_exception)
            raise family_exception

    @property
    def family_members(self):
        """
        family_members getter

        Returns
        -------
        out         : list
                      all active family_members

        """
        return self._family_members

    @family_members.setter
    def family_members(self, members: list):
        """
        family_members setter

        Parameters
        ----------
        members     : list
                      a list of family_members, i.e. of person (Male or Female) objects to append
                      to family

        """
        self._assert_family_members(members)
        self._family_members = members

    def add_family_members(self, family_members: (list, Male, Female)):
        """
        Append a list Male or Female family_member to family_members

        Parameters
        ----------
        family_members : list of Female or Male instances
                         family member to be appended

        """
        if isinstance(family_members, list):
            all(Assertor.assert_data_types([member], [Male, Female]) for member in family_members)
            self._family_members.extend(family_members)
        else:
            Assertor.assert_data_types([family_members], [Male, Female])
            self._family_members.extend([family_members])

    @property
    def inntekt(self):
        """
        income getter

        Returns
        -------
        out         : int, float
                      current gross yearly income

        """
        return self._inntekt

    @inntekt.setter
    def inntekt(self, income: (int, float, str)):
        """
        income setter

        Parameters
        ----------
        income      : int, float, str
                      new gross yearly income

        """
        Assertor.assert_data_types([income], [(int, float, str)])
        Assertor.assert_non_negative(income)
        self._inntekt = str(income)

    @property
    def antall_biler(self):
        """
        cars setter

        Returns
        -------
        out     : str
                  number of cars in the family

        """
        return self._antall_biler

    @antall_biler.setter
    def antall_biler(self, cars: (int, str)):
        """
        cars setter

        Parameters
        ----------
        cars    : int, str
                  new number of cars to set in family

        """
        Assertor.assert_data_types([cars], [(int, str)])
        Assertor.assert_non_negative(cars)
        self._antall_biler = str(cars)

    def sifo_properties(self):
        """
        return all active sifo compatible properties and values in a dictionary

        Returns
        -------
        Out     : dict
                  dictionary of all active properties

        """
        properties = dict(list(self.__dict__.items())[-2:])
        for i, family_member in enumerate(self.family_members):
            for name, prop in family_member.__dict__.items():
                if "id" not in name:
                    properties.update({name + str(i): prop})
        return {name[1:]: value for name, value in properties.items()}
