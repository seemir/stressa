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
    def run(self, col_name="Institusjon"):
        """
        method for running operation

        """
        institutions = []
        pois_location = []
        distance_air = []
        distance_walk = []
        distance_drive = []
        duration_walk = []
        duration_drive = []
        for prop, elements in self.data.items():
            if prop == "pois":
                for element in elements:

                    if "name" in element.keys():
                        institutions.append(element["name"])

                    if "coordinates" in element.keys():
                        name = element["name"] if "name" in element.keys() else ""
                        lat = element["coordinates"]["lat"]
                        long = element["coordinates"]["long"]
                        pois_location.append(
                            {col_name: name, "Breddegrad": lat, "Lengdegrad": long})

                    if "distances" in element.keys():
                        air_distance = str(element["distances"]["air"]) \
                            if element["distances"]["air"] else "0"
                        walk_distance = str(element["distances"]["walk"]) \
                            if element["distances"]["walk"] else "0"
                        drive_distance = str(element["distances"]["drive"]) \
                            if element["distances"]["drive"] else "0"
                        unit = element["distances"]["unit"]

                        distance_air.append(
                            air_distance + " " + unit if air_distance != "0" else "-")
                        distance_walk.append(
                            walk_distance + " " + unit if walk_distance != "0" else "-")
                        distance_drive.append(
                            drive_distance + " " + unit if drive_distance != "0" else "-")

                    if "duration" in element.keys():
                        if "walk" in element["duration"].keys():
                            walk_duration = element["duration"]["walk"] \
                                if element["duration"]["walk"] else 0
                            duration_walk.append(str(int(
                                round(walk_duration / 60))) + " min" if walk_duration != 0 else "-")

                        if "drive" in element["duration"].keys():
                            drive_duration = element["duration"]["drive"] \
                                if element["duration"]["drive"] else 0
                            duration_drive.append(str(int(
                                round(drive_duration / 60))) + " min" if drive_duration != 0
                                                  else "-")
                    else:
                        duration_walk.append("-")
                        duration_drive.append("-")

        inst_col, dist_col, dur_col, pois_location = self.check_data(institutions, distance_air,
                                                                     duration_walk, distance_walk,
                                                                     duration_drive, distance_drive,
                                                                     pois_location)
        identifier = self.data.copy()["id"].lower()
        return {identifier: {col_name: inst_col, "Distanse": dist_col,
                             "Tid": dur_col}, identifier + "_location": pois_location}

    @staticmethod
    def check_data(institutions, distance_air, duration_walk, distance_walk,
                   duration_drive, distance_drive, pois_location):
        """
        method for checking retrieved data

        """
        institutions_col = []
        distance_col = []
        duration_col = []
        full_line = "---------------------------------"
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
                pois_location[i].update({"Distanse (luftlinje)": distance_air[i]})
            else:
                distance_col.append("-")
                pois_location[i].update({"Distanse (luftlinje)": "-"})
            duration_col.append("-")
            institutions_col.append("Til fots")
            if distance_walk and i < len(distance_walk):
                distance_col.append(distance_walk[i])
                pois_location[i].update({"Distanse (til fots)": distance_walk[i]})
            else:
                distance_col.append("-")
                pois_location[i].update({"Distanse (til fots)": "-"})
            if duration_walk and i < len(duration_walk):
                duration_col.append(duration_walk[i])
                pois_location[i].update({"Tid (til fots)": duration_walk[i]})
            else:
                duration_col.append("-")
                pois_location[i].update({"Tid (til fots)": "-"})
            institutions_col.append("Med bil")
            if distance_drive and i < len(distance_drive):
                distance_col.append(distance_drive[i])
                pois_location[i].update({"Distanse (med bil)": distance_drive[i]})
            else:
                distance_col.append("-")
                pois_location[i].update({"Distanse (med bil)": "-"})
            if duration_drive and i < len(duration_drive):
                duration_col.append(duration_drive[i])
                pois_location[i].update({"Tid (med bil)": duration_drive[i]})
            else:
                duration_col.append("-")
                pois_location[i].update({"Tid (med bil)": "-"})
            institutions_col.append("")
            distance_col.append("")
            duration_col.append("")
        return [institutions_col, distance_col, duration_col, pois_location]
