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
                   "Andre": "Andre / uoppgitt", "0-12": "0 år - 12 år",
                   "13-18": "13 år - 18 år", "19-34": "19 år - 34 år",
                   "35-64": "35 år - 64 år", "65+": "65+ år", "NotMarried": "Ugift",
                   "Married": "Gift", "Separated": "Separert", "Widow": "Enke",
                   "0-100000": "0 - 100K", "100000-200000": "100K - 200K",
                   "200000-400000": "200K - 400K", "400000-500000": "400K - 500K",
                   "500000-800000": "500K - 800K", "800000+": "800K+"}

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
                                    self._categories[val] if val in self._categories.keys()
                                    else val)
                        elif key in ("percent", "total"):
                            for prop, elem in val.items():
                                if prop == "neighborhood":
                                    neighborhood.append(elem)
                                elif prop == "city":
                                    city.append(elem)
        data = {self.data.copy()["type"].lower(): {"Gruppe": group,
                                                   "Nabolag": neighborhood,
                                                   "By": city}}
        return data
