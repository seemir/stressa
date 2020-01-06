# -*- coding: utf-8 -*-

"""
Workflow for analysing app

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.domain import Family, Male, Female, Expenses
from source.util import Assertor, LOGGER

from ..scrapers import Sifo


class SifoWorkFlow:
    """
    Workflow for the calculation of the SIFO expenses with shares of total expenses

    """

    @staticmethod
    def populate_family(data: dict):
        """
        method for populating family information into Family object

        Returns
        -------
        out     : Family
                  Sifo compatible Family object with all necessary family information

        """
        LOGGER.disable("source.domain")
        sifo_age = {"0-5 mnd": 0.41, "6-11 mnd": 0.91, "1": 1, "2": 2, "3": 3, "4-5": 5,
                    "6-9": 9, "10-13": 13, "14-17": 17, "18-19": 19, "20-50": 50, "51-60": 60,
                    "61-66": 66, "eldre enn 66": 75}

        cars = None
        income = None
        family_members = []
        for key, val in data.items():
            if "person" in key and len(val.values()) == 2:
                age, gender = sifo_age[list(val.values())[0]], list(val.values())[1]
                family_member = Male(age) if gender == "Mann" else Female(age)
                family_members.append(family_member)
            elif "brutto_arsinntekt" in key:
                income = val.replace(" kr", "").replace(" ", "")
            elif "antall_biler" in key:
                cars = val
            else:
                pass
        if family_members:
            family_income = income if income else 0
            family_num_cars = cars if cars else 0
            family = Family(family_members, family_income, family_num_cars)
        else:
            family = None
        LOGGER.enable("source.domain")
        return family

    def __init__(self, data: dict):
        """

        Parameters
        ----------
        data    : dict
                  information about the family, i.e. arguments to be passed to Family object

        """
        Assertor.assert_data_types([data], [dict])
        self._data = data
        self._family = self.populate_family(self.data)
        self._sifo = Sifo(self.family) if self.family else None
        self._base_expenses = Expenses(
            self.sifo.sifo_base_expenses()) if self.sifo else None
        self._expenses_value = self.base_expenses.expenses_values if \
            self.base_expenses else None
        self._expenses_share = self.base_expenses.expenses_shares if \
            self.base_expenses else None

    @property
    def data(self):
        """
        data getter

        Returns
        -------
        out     : dict
                  active _data property

        """
        return self._data

    @property
    def family(self):
        """
        family object getter

        Returns
        -------
        out     : Family
                  active _family property

        """
        return self._family

    @property
    def sifo(self):
        """
        sifo object getter

        Returns
        -------
        out     : Sifo
                  active _sifo object

        """
        return self._sifo

    @property
    def base_expenses(self):
        """
        base expenses getter, i.e. expenses as returned from Sifo.sifo_base_expenses() method

        Returns
        -------
        out     : Expenses
                  active _sifo_base_expenses object

        """
        return self._base_expenses

    @property
    def expenses_value(self):
        """
        gets the sifo expenses values in NOK

        Returns
        -------
        out     : dict
                  active _expenses_values

        """
        return self._expenses_value

    @property
    def expenses_share(self):
        """
        gets the sifo expenses values as a percent of total

        Returns
        -------
        out     : dict
                  active _expenses_shares

        """
        return self._expenses_share
