# -*- coding: utf-8 -*-

"""
Family entity class implementation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from typing import Union

from source.util import Assertor, Debugger

from .entity import Entity
from .female import Female
from .male import Male


class Family(Entity):
    """
    Family entity class

    """

    @staticmethod
    def validate_family_members(family_members: list):
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

    @staticmethod
    def validate_income(income: Union[int, float, str]):
        """
        method for validating that income is non-negative

        Parameters
        ----------
        income          : int, float, str
                          income to be validated

        """
        Assertor.assert_data_types([income], [(int, float, str)])
        Assertor.assert_non_negative([income], msg="Only non-negative 'income' accepted")

    @staticmethod
    def validate_select_year(select_year: Union[int, str]):
        """
        method for validating selected budget year

        Parameters
        ----------
        select_year     : int, str
                          budget year

        """
        if not select_year:
            raise ValueError("Expected a 'budsjett aar', got '{}' "
                             "".format(select_year.__class__.__name__))

    @staticmethod
    def validating_cars(cars: Union[int, str]):
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
                 fossil_cars: Union[int, str] = 0, electric_cars: Union[int, str] = 0,
                 select_year: Union[int, str] = None):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        family_members  : list
                          list of Person (Male or Female) instances
        income          : int, float, str
                          gross yearly income
        fossil_cars     : int, str
                          number of fossil cars in the family
        electric_cars   : int, str
                          number of electric cars in the family
        select_year     : int, str
                          budget year

        """
        super().__init__()
        self.validate_family_members(family_members)
        self.validate_income(income)
        self.validating_cars(fossil_cars)
        self.validating_cars(electric_cars)
        self.validate_select_year(select_year)

        self._familie_medlemmer = family_members
        self._inntekt = str(income)
        self._antall_biler = str(fossil_cars)
        self._antall_elbiler = str(electric_cars)
        self._select_year = str(select_year)

    @property
    def familie_medlemmer(self):
        """
        family_members getter

        Returns
        -------
        out         : list
                      all active family_members

        """
        return self._familie_medlemmer

    @familie_medlemmer.setter
    def familie_medlemmer(self, new_members: list):
        """
        family_members setter

        Parameters
        ----------
        new_members     : list
                          a list of family_members, i.e. of person (Male or Female) objects to
                          append to family

        """
        self.validate_family_members(new_members)
        self._familie_medlemmer = new_members

    @Debugger
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
            self._familie_medlemmer.extend(family_members)
        else:
            Assertor.assert_data_types([family_members], [Male, Female])
            self._familie_medlemmer.extend([family_members])

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
        self.validate_income(income)
        self._inntekt = str(income)

    @property
    def antall_biler(self):
        """
        fossil cars setter

        Returns
        -------
        out     : str
                  number of cars in the family

        """
        return self._antall_biler

    @antall_biler.setter
    def antall_biler(self, cars: (int, str)):
        """
        fossile cars setter

        Parameters
        ----------
        cars    : int, str
                  new number of cars to set in family

        """
        self.validating_cars(cars)
        self._antall_biler = str(cars)

    @property
    def antall_elbiler(self):
        """
        electric cars setter

        Returns
        -------
        out     : str
                  number of cars in the family

        """
        return self._antall_elbiler

    @antall_elbiler.setter
    def antall_elbiler(self, cars: (int, str)):
        """
        electric cars setter

        Parameters
        ----------
        cars    : int, str
                  new number of cars to set in family

        """
        self.validating_cars(cars)
        self._antall_elbiler = str(cars)

    @property
    def select_year(self):
        """
        select year getter

        Returns
        -------
        out     : int, str
                  selected budget year

        """
        return self._select_year

    @select_year.setter
    def select_year(self, new_year):
        """
        select year setter

        """
        self.validate_select_year(new_year)
        self._select_year = new_year

    @Debugger
    def sifo_properties(self):
        """
        return all active sifo compatible properties and values in a dictionary

        Returns
        -------
        Out     : dict
                  dictionary of all active properties

        """
        properties = dict(list(self.__dict__.items())[-4:])

        for i, family_member in enumerate(self.familie_medlemmer):
            for name, prop in family_member.__dict__.items():
                if "_id" not in name:
                    properties.update({name + str(i): prop})
        prop = {name[1:]: value for name, value in properties.items()}

        return prop

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
