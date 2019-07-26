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

    def __init__(self, family_members):
        for family_member in family_members:
            if not isinstance(family_member, (Male, Female)):
                raise TypeError(
                    "family_member can only be of instance 'Male' or 'Female', got {}".format(
                        family_member.__class__))
        self.family_members = family_members

    def get_properties(self, prop_name):
        """
        Get all properties of all family members

        Parameters
        ----------
        prop_name    : str

        Returns
        -------
        Out          : list
                       property of all members in family as SIFO compatible string

        """
        properties = {}
        for i, family_member in enumerate(self.family_members):
            try:
                properties.update({prop_name + str(i): getattr(family_member, prop_name)})
            except Exception as error:
                if prop_name == 'pregnant':
                    properties.update({prop_name + str(i): '0'})
                else:
                    raise error
        return properties

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
