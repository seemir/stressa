# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util.evaluator import Evaluator
from source.domain.female import Female
from source.domain.male import Male


class Family:
    """
    Family class, i.e. list of Male and Female instances

    """

    def __init__(self, family_members, income=0, cars=0):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        family_members  : list
                          list of Person (Male or Female) instances
        income          : int, float
                          gross yearly income
        """
        if not isinstance(family_members, list):
            raise TypeError(
                "expected type '{}', got '{}' instead".format(list.__name__,
                                                              type(family_members).__name__))
        Evaluator.evaluate_data_type({income: (int, float), cars: int})

        for family_member in family_members:
            if not isinstance(family_member, (Male, Female)):
                raise TypeError(
                    "family_member can only be of instance 'Male' or 'Female', got {}".format(
                        family_member.__class__))

        self.family_members = family_members
        self.inntekt = str(income)
        self.antall_biler = str(cars)

    def add_family_member(self, family_member):
        """
        Append a Male or Female family_member to family_members

        Parameters
        ----------
        family_member : Male, Female
                        family member to be appended

        """
        Evaluator.evaluate_data_type({family_member: (Male, Female)})
        self.family_members.append(family_member)

    def get_properties(self):
        """
        return all active properties and values in a dictionary

        Returns
        -------
        Out     : dict
                  dictionary of all active properties

        """
        properties = dict(list(self.__dict__.items())[-2:])
        for i, family_member in enumerate(self.family_members):
            properties.update(
                {fam_member + str(i): prop_value for fam_member, prop_value in
                 family_member.get_properties().items()})
        return properties
