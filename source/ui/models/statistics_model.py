# -*- coding: utf-8 -*-
"""
Module of the Statistics model which handles all the statistics from Finn Ad

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from PyQt5.QtCore import QObject

from source.util import Assertor

from .model import Model


class StatisticsModel(Model):
    """
    Implementation of the Statistics model for which all the Finn based statistics logic is stored

    """
    _statistics_keys = ["finnkode", "first_published", "location", "property_type", "price_range",
                        "prisantydning", "sqm_price", "city_area_sqm_price",
                        "municipality_sqm_price", "size_range", "primrrom", "bruttoareal", "views",
                        "ad_of_the_week", "normal_traffic", "email_sent", "favorite_click",
                        "add_to_calendar", "prospect_viewed", "prospect_ordered",
                        "city_area_sqm_price", "municipality_sqm_price", "city_area",
                        "municipality"]

    def __init__(self, parent: QObject):
        """
        Constructor / Instantiation of class

        Parameters
        ----------
        parent      : QObject
                      Parent view for which the model in to be linked

        """
        Assertor.assert_data_types([parent], [QObject])
        super().__init__(parent)

    def add_statistics_info(self, postfix):
        """
        method for adding statistics info to StatisticsModel

        Parameters
        ----------
        postfix     : str
                      index if used in naming of line_edits

        """
        Assertor.assert_data_types([postfix], [str])
        grandparent = self.parent.parent
        statistics_data = {}
        if grandparent.finn_model.finn_data:
            for key, val in grandparent.finn_model.finn_data.items():
                if key[:-len(postfix)] in self._statistics_keys:
                    statistics_data.update({key: val})
        self.data.update(statistics_data)
        for key in self._statistics_keys:
            if key + postfix in self.data.keys():
                if key in ["city_area", "municipality"]:
                    getattr(self.parent.ui, "label_" + key + "_sqm_price").setText(
                        "KMP ({})".format(self.data[key + postfix]))
                else:
                    getattr(self.parent.ui, "line_edit_" + key).setText(self.data[key + postfix])
            else:
                if key not in ["municipality", "city_area"]:
                    getattr(self.parent.ui, "line_edit_" + key).clear()

    def clear_statistics_info(self, postfix):
        """
        method for clearing finn statistics from line_edit

        Parameters
        ----------
        postfix     : str
                      index if used in naming of line_edits

        """
        Assertor.assert_data_types([postfix], [str])
        grandparent = self.parent.parent.finn_model
        for key in self._statistics_keys:
            full_key = key + postfix
            if full_key in self.data.keys():
                self.data.pop(full_key)
            if full_key in grandparent.data.keys():
                grandparent.data.pop(full_key)
            if full_key in grandparent.finn_data.keys():
                grandparent.finn_data.pop(full_key)

            if key == "city_area":
                self.parent.label_city_area_sqm_price.setText("KMP (område)")
            elif key == "municipality":
                self.parent.label_municipality_sqm_price.setText("KMP (kommune)")
            else:
                getattr(self.parent.ui, "line_edit_" + key).clear()
