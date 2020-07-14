# -*- coding: utf-8 -*-
"""
Restructuring Ratings Operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Tracking

from .restructure import Restructure


class RestructureRatings(Restructure):
    """
    Operation for restructuring Ratings

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
        method for running the operation

        """
        neighborhood_text = []
        neighborhood_score = []
        city_text = []
        city_score = []

        for keys, values in self.data.items():
            if keys == "rating_kindergardens":
                for key, value in values.items():
                    if key == "text":
                        neighborhood_text.append(value)
                    elif key == "neighborhood":
                        neighborhood_score.append(value)
                    elif key == "city":
                        city_score.append(value)
                    elif key == "cityText":
                        city_text.append(value)
            elif keys == "rating_schools":
                for key, value in values.items():
                    if key == "text":
                        neighborhood_text.append(value)
                    elif key == "neighborhood":
                        neighborhood_score.append(value)
                    elif key == "city":
                        city_score.append(value)
                    elif key == "cityText":
                        city_text.append(value)

        full_line = "------------------------"
        group = ["Vurdering:", full_line, "Barnehage", "Skolene", ""]
        neighborhood_column = ["", ""]
        city_column = ["", ""]

        for i, text in enumerate(neighborhood_text):
            if text and city_text[i]:
                neighborhood_column.append("{} ({})".format(str(neighborhood_score[i]), text))
                city_column.append("{} ({})".format(str(city_score[i]), city_text[i]))
            else:
                neighborhood_column.append("NA")
                city_column.append("NA")

        neighborhood_column = neighborhood_column + [""]
        city_column = city_column + [""]

        return {"Gruppe": group, "Nabolag": neighborhood_column, "By": city_column}
