# -*- coding: utf-8 -*-
"""
Module containing operation for restructuring score JSON

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Tracking

from .restructure import Restructure


class RestructureScore(Restructure):
    """
    Operation for restructuring Score JSON

    """

    @Tracking
    def __init__(self, data: dict, desc: str, key: str):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        data        : dict
                      data to be restructured
        desc        : str
                      description of operation

        """
        super().__init__(data=data, desc=desc)
        self.key = key if key else "Vurdering:"

    @Tracking
    def run(self):
        """
        method for running operation

        """
        group = []
        score = []

        for key, val in self.data.items():
            if key == 'data':
                for element in val:
                    if "group" in element.keys():
                        group.append(element["group"])
                    if "percent" in element.keys():
                        if "neighborhood" in element["percent"].keys():
                            score.append(round(element["percent"]["neighborhood"] * 100, 3))

        full_line = "-------------"
        group_column = [self.key, full_line] + group + [""]
        score_column = ["", ""] + score + [""]

        return {self.data.copy()["id"].lower(): {"Gruppe": group_column, "Score": score_column}}
