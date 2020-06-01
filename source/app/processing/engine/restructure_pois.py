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
                                    if key == "walk":
                                        duration_walk.append(str(int(round(value / 60))) + " min")
                                    elif key == "drive":
                                        duration_drive.append(str(int(round(value / 60))) + " min")
        institutions_col = []
        distance_col = []
        duration_col = []
        full_line = "----------------------"
        half_line = "- - - - - - - - - - - "
        for i, val in enumerate(institutions):
            if i == 0:
                institutions_col.append(full_line)
                distance_col.append(full_line)
                duration_col.append(full_line)
            else:
                institutions_col.append(institutions[i])
                distance_col.append("")
                duration_col.append("")
                institutions_col.append(half_line)
                distance_col.append(half_line)
                duration_col.append(half_line)
                institutions_col.append("Luftlinje")
                distance_col.append(distance_air[i])
                duration_col.append("-")
                institutions_col.append("Til fots")
                distance_col.append(distance_walk[i])
                duration_col.append(duration_walk[i])
                institutions_col.append("Med bil")
                distance_col.append(distance_drive[i])
                duration_col.append(duration_drive[i])
                institutions_col.append(full_line)
                distance_col.append(full_line)
                duration_col.append(full_line)
        data = {self.data.copy()["type"].lower(): {"Institusjon": institutions_col,
                                                   "Distanse": distance_col,
                                                   "Tid": duration_col}}
        return data
