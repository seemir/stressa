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

    requirements_mortgage = ['personinntekt_total_aar', 'egenkapital', 'intervall', 'laneperiode',
                             'lanetype', 'betjeningsevne', 'startdato']
    requirements_restructure = requirements_mortgage + ['belaning']

    def validate_mortgage_information(self, data: dict, restructure=False):
        """
        method for validating mortgage information

        Parameters
        ----------
        data        : dict
                      mortgage information
        restructure : bool
                      restructure data to validate

        """
        Assertor.assert_data_types([data], [dict])
        if restructure:
            if not all(element in data.keys() for element in self.requirements_restructure):
                raise ValueError(
                    f"all element in '{self.requirements_restructure}' must be supplied "
                    f"for restructure")
            final = {}
            if "nominell_rente" in data.keys():
                final.update({"nominell_rente": data["nominell_rente"]})
            final.update({key: val for key, val in data.items() if key in
                          self.requirements_restructure})
        else:
            if not all(element in data.keys() for element in self.requirements_mortgage):
                raise ValueError(
                    f"all element in '{self.requirements_mortgage}' must be supplied for mortgage")
            final = {key: val for key, val in data.items() if key in self.requirements_mortgage}
        return final

    def __init__(self, data: dict, restructure=False):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        data        : dict
                      mortgage information

        """
        super().__init__()
        self._mortgage_data = self.validate_mortgage_information(data)
        self._restructure_data = self.validate_mortgage_information(data, restructure)

    @property
    def restructure_data(self):
        """
        restructure_data getter

        Returns
        -------
        out         : dict
                      restructure data

        """
        return self._restructure_data

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
    def rules(restructure=False):
        """
        all active validation rules in entity

        Returns
        -------
        out         : dict
                      dictionary with all the active rules in the entity

        """
        mortgage_data = ['personinntekt_total_aar', 'egenkapital', 'intervall', '\\nlaneperiode',
                         'lanetype', 'betjeningsevne', 'startdato']
        restructure_data = mortgage_data + ['belaning']
        mortgage_property = "mortgage " if not restructure else "restructure "
        mortgage_rules = ", ".join(mortgage_data if not restructure else restructure_data).replace(
            "'", "")

        return f"{mortgage_property} contains '{mortgage_rules}'"
