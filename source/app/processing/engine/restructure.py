# -*- coding: utf-8 -*-
"""
Module containing operation for restructuring Community / Nabolag JSON

"""

__author__ = 'Samir Adrik'
__email__ = 'saÿmir.adrik@gmail.com'

from source.util import Tracking, Assertor

from .operation import Operation


class Restructure(Operation):
    """
    Operation for restructuring Community / Nabolag JSON

    """

    _categories = {"AllmenneFag": "Allmennefaglig", "HelseSosial": "Helse og sosial",
                   "Okonomiske": "Økonomiske fag", "NatVit": "Naturvitenskapelig",
                   "HumanEstetikk": "Human og estetikk", "Samfunn": "Samfunnsfaglig",
                   "Laerer": "Lærerutdanning", "Primaer": "Primærnæring",
                   "Andre": "Andre / uoppgitt",
                   "0-12": "0 år - 12 år", "13-18": "13 år - 18 år", "19-34": "19 år - 34 år",
                   "35-64": "35 år - 64 år", "65+": "65+ år",
                   "0-5": "0 år - 5 år", "6-12": "6 år - 12 år",
                   "13-15": "13 år - 15 år", "16-18": "16 år - 18 år",
                   "NotMarried": "Ugift", "Married": "Gift", "Separated": "Separert",
                   "Widow": "Enke",
                   "0-100000": "0 - 100K", "100000-200000": "100K - 200K",
                   "200000-400000": "200K - 400K", "400000-500000": "400K - 500K",
                   "500000-800000": "500K - 800K", "800000+": "800K+",
                   "0-2000000": "0 - 2 mill", "2000000-3000000": "2 mill - 3 mill",
                   "3000000-4000000": "3 mill - 4 mill", "4000000-5000000": "4 mill - 5 mill",
                   "5000000-6000000": "5 mill - 6 mill", "6000000+": "6 mill+",
                   "CouplesWithChildren": "Par med barn", "CouplesWithoutChildren": "Par uten barn",
                   "SingleWithChildren": "Single med barn", "MultiFamilies": "Flerfamilie",
                   "SingleWithoutChildren": "Single uten barn",
                   "owns": "Eier",
                   "rents": "Leier",
                   "0-60": "0 - 60 m\u00b2",
                   "60-120": "60 m\u00b2 - 120 m\u00b2",
                   "120-200": "120 m\u00b2 - 200 m\u00b2",
                   "200+": "200 m\u00b2+",
                   "0-10": "0 år - 10 år",
                   "10-30": "10 år - 30 år",
                   "30-50": "30 år - 50 år",
                   "50+": "50+ år"}

    @Tracking
    def __init__(self, data: dict, desc: str):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        data        : dict
                      data to be restructured
        desc        : str
                      description of operation

        """
        self.name = self.__class__.__name__
        Assertor.assert_data_types([data, desc], [dict, str])
        super().__init__(name=self.name, desc="id: {}".format(desc))
        self.data = data

    @Tracking
    def run(self):
        """
        method for running operation

        """
        group = []
        neighborhood = []
        city = []
        for keys, values in self.data.items():
            if keys in ("values", "stats"):
                for value in values:
                    for key, val in value.items():
                        if key == "group":
                            if val == "People":
                                group.append("Befolkning")
                            elif val == "Households":
                                group.append("Husholdninger")
                            else:
                                group.append(
                                    self._categories[val].capitalize()
                                    if val in self._categories.keys() else val.capitalize())
                        elif key in ("percent", "total"):
                            for prop, elem in val.items():
                                if prop == "neighborhood":
                                    neighborhood.append(elem)
                                elif prop == "city":
                                    city.append(elem)
        data = {self.data.copy()["id"].lower(): {"Gruppe": group,
                                                 "Nabolag": neighborhood,
                                                 "By": city if city else [0 for _ in range(
                                                     len(neighborhood))]}}
        return data
