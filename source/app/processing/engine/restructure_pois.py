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
                                    distance = str(value) + " " + values["unit"] if value else "-"
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
                                        duration_walk.append(
                                            str(int(round(value / 60))) + " min" if value else "-")
                                    elif key == "drive":
                                        duration_drive.append(
                                            str(int(round(value / 60))) + " min" if value else "-")
        institutions_col = []
        distance_col = []
        duration_col = []
        full_line = "----------------------"
        for i, _ in enumerate(institutions):
            institutions_col.append(institutions[i])
            distance_col.append("")
            duration_col.append("")
            institutions_col.append(full_line)
            distance_col.append("")
            duration_col.append("")
            institutions_col.append("Luftlinje")
            if distance_air and i < len(distance_air):
                distance_col.append(distance_air[i])
            else:
                distance_col.append("-")
            duration_col.append("-")
            institutions_col.append("Til fots")
            if distance_walk and i < len(distance_walk):
                distance_col.append(distance_walk[i])
            else:
                distance_col.append("-")
            if duration_walk and i < len(duration_walk):
                duration_col.append(duration_walk[i])
            else:
                duration_col.append("-")
            institutions_col.append("Med bil")
            if distance_drive and i < len(distance_drive):
                distance_col.append(distance_drive[i])
            else:
                distance_col.append("-")
            if duration_drive and i < len(duration_drive):
                duration_col.append(duration_drive[i])
            else:
                duration_col.append("-")
            institutions_col.append("")
            distance_col.append("")
            duration_col.append("")
        data = {self.data.copy()["type"].lower(): {"Institusjon": institutions_col,
                                                   "Distanse": distance_col,
                                                   "Tid": duration_col}}
        return data
