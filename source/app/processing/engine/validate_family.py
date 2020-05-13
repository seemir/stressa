# -*- coding: utf-8 -*-

"""
Module for Operation for Populating Family Entity with information from SifoView

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.domain import Family, Male, Female
from source.util import Assertor, Tracking

from .operation import Operation


class ValidateFamily(Operation):
    """
    Implementation of Populate Family Entity operation

    """
    sifo_arg = {"0-5 mnd": 0.41, "6-11 mnd": 0.91, "1": 1, "2": 2, "3": 3, "4-5": 5,
                "6-9": 9, "10-13": 13, "14-17": 17, "18-19": 19, "20-50": 50, "51-60": 60,
                "61-66": 66, "eldre enn 66": 75}
    barnehage_arg = {"Nei": "0", "Ja": "1"}
    sfo_arg = {"Nei": "0", "Halvdag": "1", "Heldag": "2"}

    @Tracking
    def __init__(self, data: dict):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        data    : dict
                  Sifo compatible dictionary with all necessary family information

        """
        self.name = self.__class__.__name__
        Assertor.assert_data_types([data], [dict])
        super().__init__(name=self.name,
                         desc="rules: {} \\n id: Validate Family Information".format(
                             Family.rules()))
        self.data = data

    @Tracking
    def run(self):
        """
        method for running operation

        Returns
        -------
        out     : Family
                  Sifo compatible Family object with all necessary family information

        """
        family_members = []
        cars = None
        income = None
        for key, val in self.data.items():
            if "person" in key:
                arg = {}
                gender = None
                for prop, value in val.items():
                    if "alder" in prop:
                        arg.update({"age": self.sifo_arg[value]})
                    elif "kjonn" in prop:
                        gender = Male if "Mann" in value else Female
                    elif "barnehage" in prop:
                        arg.update({"kinder_garden": self.barnehage_arg[value]})
                    elif "sfo" in prop:
                        arg.update({"sfo": self.sfo_arg[value]})
                    elif "gravid" in prop:
                        arg.update({"pregnant": self.barnehage_arg[value]})
                if gender and arg:
                    family_member = gender(**arg)
                    family_members.append(family_member)
            elif "brutto_arsinntekt" in key:
                income = val.replace(" kr", "").replace(" ", "")
            elif "antall_biler" in key:
                cars = val
        family_income = income if income else 0
        family_num_cars = cars if cars else 0
        family = Family(family_members, family_income, family_num_cars)
        return family
