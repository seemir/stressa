# -*- coding: utf-8 -*-

"""
Workflow for analysing app

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.domain import Family, Male, Female
from source.util import Assertor

from ..scrapers import Sifo


class SifoWorkFlow:
    """
    Workflow for the calculation of the SIFO expenses with shares of total expenses

    """
    sifo_age = {"0-5 mnd": 0.41, "6-11 mnd": 0.91, "1": 1, "2": 2, "3": 3, "4-5": 5,
                "6-9": 9, "10-13": 13, "14-17": 17, "18-19": 19, "20-50": 50, "51-60": 60,
                "61-66": 66, "eldre enn 66": 75}

    def __init__(self, data: dict):
        """

        Parameters
        ----------
        data    : dict
                  information about the family, i.e. arguments to be passed to Family object

        """
        Assertor.assert_data_types([data], [dict])
        self._data = data
        self._family = None

    @property
    def data(self):
        """
        Data getter

        Returns
        -------
        out     : dict
                  active _data property

        """
        return self._data

    @property
    def family(self):
        """
        Family getter

        Returns
        -------
        out     : Family
                  active _family property

        """
        return self._family

    def populate_family(self):
        """
        method for populating family information into Family object

        Returns
        -------
        out     : Family
                  Sifo compatible Family object with all necessary family information

        """
        cars = None
        income = None
        family_members = []
        for key, val in self.data.items():
            if "person" in key and len(val.values()) == 2:
                age, gender = self.sifo_age[list(val.values())[0]], list(val.values())[1]
                family_member = Male(age) if gender == "Mann" else Female(age)
                family_members.append(family_member)
            elif "brutto_arsinntekt" in key:
                income = val
            elif "antall_biler" in key:
                cars = val
            else:
                pass
        if family_members and income and cars:
            family = Family(family_members, income, cars)
        elif family_members and income:
            family = Family(family_members, income)
        elif family_members:
            family = Family(family_members)
        else:
            family = None
        return family

    def get_base_sifo_expenses(self):
        """
        method for getting Sifo base expenses

        Returns
        -------
        out     : dict
                  dictionary with all base sifo expenses

        """
        sifo = Sifo(self.populate_family())
        return sifo.sifo_expenses()
