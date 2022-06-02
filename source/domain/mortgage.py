# -*- coding: utf-8 -*-

"""
Mortgage entity class

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor

from source.domain.entity import Entity


class Mortgage(Entity):
    """
    Mortgage entity class

    """

    requirements = ['brutto_inntekt_total', 'egenkapital', 'intervall', 'laneperiode',
                    'lanetype', 'netto_likviditet', 'startdato']

    def validate_mortgage_information(self, data: dict):
        """
        method for validating mortgage information

        Parameters
        ----------
        data        : dict
                      mortgage information

        """
        Assertor.assert_data_types([data], [dict])
        if not all(element in data.keys() for element in self.requirements):
            raise ValueError(
                "all element in '{}' must be supplied for mortgage".format(self.requirements))
        return {key: val for key, val in data.items() if key in self.requirements}

    def __init__(self, data: dict):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        data        : dict
                      mortgage information

        """
        super().__init__()
        self._mortgage_data = self.validate_mortgage_information(data)

    @property
    def mortgage_data(self):
        """
        mortgage_data getter

        Returns
        -------
        out         : dict
                      mortgage data

        """
        return self._mortgage_data

    @mortgage_data.setter
    def mortgage_data(self, new_mortgage_data: dict):
        """
        mortgage_data setter

        Parameters
        ----------
        new_mortgage_data   : dict
                              new mortgage data

        """
        self._mortgage_data = self.validate_mortgage_information(new_mortgage_data)

    @staticmethod
    def rules():
        """
        all active validation rules in entity

        Returns
        -------
        out         : dict
                      dictionary with all the active rules in the entity

        """
        return "mortgage contains '{}'".format(
            ", ".join(
                ['brutto_inntekt_total', 'egenkapital', 'intervall', '\\nlaneperiode', 'lanetype',
                 'netto_likviditet', 'startdato']).replace("'", ""))
