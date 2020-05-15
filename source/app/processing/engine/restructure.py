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
                                group.append(val)
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
