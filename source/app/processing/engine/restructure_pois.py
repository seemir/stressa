# -*- coding: utf-8 -*-
"""
Restructuring Operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Tracking

from .restructure import Restructure


class RestructurePois(Restructure):
    """
    Operation for restructuring Higher institutional data

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
        super().__init__(data=data, desc=desc)

    @Tracking
    def run(self):
        """
        method for running operation

        """
        institutions = []
        distance_air = []
        distance_walk = []
        distance_drive = []
        duration_walk = []
        duration_drive = []
        measure_text = []
        for prop, elements in self.data.items():
            if prop == "pois":
                for element in elements:
                    for keys, values in element.items():
                        if keys == "name":
                            institutions.append(values)
                        elif keys == "distances":
                            if "unit" in values.keys():
                                for key, value in values.items():
                                    distance = str(value) + " " + values["unit"]
                                    if key == "air":
                                        distance_air.append(distance)
                                    elif key == "drive":
                                        distance_drive.append(distance)
                                    elif key == "walk":
                                        distance_walk.append(distance)
                        elif keys == "duration":
                            if "unit" in values.keys():
                                for key, value in values.items():
                                    duration = str(value) + " " + values["unit"]
                                    if key == "walk":
                                        duration_walk.append(duration)
                                    elif key == "drive":
                                        duration_drive.append(duration)
                        elif keys == "measureText":
                            measure_text.append(values)
        data = {self.data.copy()["type"].lower(): {"Institusjon": institutions,
                                                   "Distanse (luftlinje)": distance_air,
                                                   "Distanse (til fots)": distance_walk,
                                                   "Distanse (med bil)": distance_drive,
                                                   "Varighet (til fots)": duration_walk,
                                                   "Varighet (med bil)": duration_drive,
                                                   "Varihet (min)": measure_text}}
        return data
