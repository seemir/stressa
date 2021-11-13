# -*- coding: utf-8 -*-

"""
Family entity class implementation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from typing import Union

from source.util import Assertor, Tracking

from .entity import Entity
from .female import Female
from .male import Male


class Family(Entity):
    """
    Family entity class

    """

    @Tracking
    def validate_family_members(self, family_members: list):
        """
        Validate the family_members object. In this implementation a Family has the following
        characteristics:

        - Needs to be a list
        - All objects in the list must be either of class Male or Female

        Parameters
        ----------
        family_members  : list
                          list of Male or Female objects

        """
        Assertor.assert_data_types([family_members], [list])

        for family_member in family_members:
            Assertor.assert_data_types([family_member], [(Male, Female)])

    @Tracking
    def validate_income(self, income: Union[int, float, str]):
        """
        method for validating that income is non-negative

        Parameters
        ----------
        income          : int, float, str
                          income to be validated

        """
        Assertor.assert_data_types([income], [(int, float, str)])
        Assertor.assert_non_negative([income], msg="Only non-negative 'income' accepted")

    @Tracking
    def validating_cars(self, cars: Union[int, str]):
        """
        method for validating that number of cars is non-negative

        Parameters
        ----------
        cars          : int, str
                        number of cars to be validated

        """
        Assertor.assert_data_types([cars], [(int, str)])
        Assertor.assert_non_negative([cars], msg="Only non-negative 'numbers of cars'")

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
        self.validate_family_members(family_members)
        self.validate_income(income)
        self.validating_cars(cars)

        self._family_members = family_members
        self._income = str(income)
        self._cars = str(cars)

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
    def family_members(self, new_members: list):
        """
        family_members setter

        Parameters
        ----------
        new_members     : list
                          a list of family_members, i.e. of person (Male or Female) objects to
                          append to family

        """
        self.validate_family_members(new_members)
        self._family_members = new_members

    @Tracking
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
    def income(self):
        """
        income getter

        Returns
        -------
        out         : int, float
                      current gross yearly income

        """
        return self._income

    @income.setter
    def income(self, income: (int, float, str)):
        """
        income setter

        Parameters
        ----------
        income      : int, float, str
                      new gross yearly income

        """
        self.validate_income(income)
        self._income = str(income)

    @property
    def cars(self):
        """
        cars setter

        Returns
        -------
        out     : str
                  number of cars in the family

        """
        return self._cars

    @cars.setter
    def cars(self, cars: (int, str)):
        """
        cars setter

        Parameters
        ----------
        cars    : int, str
                  new number of cars to set in family

        """
        self.validating_cars(cars)
        self._cars = str(cars)

    @Tracking
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
                if "_id" not in name:
                    properties.update({name + str(i): prop})
        return {name[1:]: value for name, value in properties.items()}

    @staticmethod
    def rules():
        """
        list of all rules in this entity

        Returns
        -------
        out         : list
                      all rules in entity

        """
        return ", ".join(
            ['non_negative_income', 'non_negative_cars', 'kindergarten_criteria', 'sfo_criteria',
             'pregnant_criteria']).replace("'", "")
