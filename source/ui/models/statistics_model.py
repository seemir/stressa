# -*- coding: utf-8 -*-
"""
Module of the Statistics model which handles all the statistics from the Finn Adverts

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from PyQt5.QtCore import QObject

from source.util import Assertor
from source.ui.graphics import BarChart, DoubleBarChart, ErrorBarPlot

from .model import Model


class StatisticsModel(Model):
    """
    Implementation of the Statistics model for which all the Finn based statistics logic is stored

    """
    _statistics_keys = ["finnkode", "first_published", "location", "property_type", "price_range",
                        "prisantydning", "sqm_price", "city_area_sqm_price",
                        "municipality_sqm_price", "size_range", "primrrom", "bruttoareal",
                        "ad_of_the_week", "normal_traffic", "totalviews", "latestemailcount",
                        "currentfavorites", "city_area_sqm_price", "municipality_sqm_price",
                        "city_area", "municipality", "hist_data_city_area",
                        "hist_data_municipality", "hist_data_city_area_count",
                        "hist_data_municipality_count", "views_development", "baseline"]

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
        self.sales_plot = None
        self.view_plot = None
        self.error_plot = None

    def add_statistics_info(self, postfix: str):
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
        prefix = "graphics_view_"
        if grandparent.finn_model.finn_data:
            for key, val in grandparent.finn_model.finn_data.items():
                if key[:-len(postfix)] in self._statistics_keys:
                    statistics_data.update({key: val})
        self.data.update(statistics_data)
        for key in self._statistics_keys:
            if key == "hist_data_municipality":
                if key + postfix in self.data.keys() and self.data[key + postfix]:
                    BarChart.clear_graphics(
                        getattr(self.parent.ui, prefix + "hist_data_municipality"))
                    BarChart.clear_graphics(getattr(self.parent.ui, prefix + "hist_data_city_area"))
                    self.add_sqm_dist_charts(prefix, postfix)
            elif key in ["hist_data_city_area", "baseline"]:
                pass
            elif key == "views_development":
                if key + postfix in self.data.keys() and self.data[key + postfix]:
                    DoubleBarChart.clear_graphics(
                        getattr(self.parent.ui, prefix + "views_development"))
                    DoubleBarChart.clear_graphics(
                        getattr(self.parent.ui, prefix + "accumulated"))
                    ErrorBarPlot.clear_graphics(getattr(self.parent.ui, prefix + "baseline"))
                    self.add_view_charts(prefix, postfix)
            else:
                if key + postfix in self.data.keys():
                    self.add_statistics_label(key, postfix)
                else:
                    if key not in ["municipality", "city_area"]:
                        getattr(self.parent.ui, "line_edit_" + key).clear()
        for graphics_view in ["hist_data_city_area", "hist_data_municipality", "views_development",
                              "accumulated", "baseline", "some_statistics"]:
            getattr(self.parent.ui, prefix + graphics_view).setMouseEnabled(x=False, y=False)
            getattr(self.parent.ui, prefix + graphics_view).getAxis('left').setStyle(
                showValues=False)
            getattr(self.parent.ui, prefix + graphics_view).getAxis('bottom').setStyle(
                showValues=False)

    def clear_statistics_info(self, postfix: str):
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
                self.parent.label_sales_city_area.setText("Salg (område)")
            elif key == "municipality":
                self.parent.label_municipality_sqm_price.setText("KMP (kommune)")
                self.parent.label_sales_municipality.setText("Salg (kommune)")
            elif key == "hist_data_city_area":
                BarChart.clear_graphics(self.parent.ui.graphics_view_hist_data_city_area)
            elif key == "hist_data_municipality":
                BarChart.clear_graphics(self.parent.ui.graphics_view_hist_data_municipality)
            elif key == "views_development":
                DoubleBarChart.clear_graphics(self.parent.graphics_view_views_development)
                DoubleBarChart.clear_graphics(self.parent.graphics_view_accumulated)
            elif key == "baseline":
                ErrorBarPlot.clear_graphics(self.parent.graphics_view_baseline)
            else:
                getattr(self.parent.ui, "line_edit_" + key).clear()

    def add_sqm_dist_charts(self, prefix: str, postfix: str):
        """
        method for adding square meter distribution chart to the statistics model

        Parameters
        ----------
        prefix      : str
                      name of prefix, i.e. "graphics"
        postfix     : str
                      index if used in naming of line_edits

        """
        Assertor.assert_data_types([prefix, postfix], [str, str])
        city_area_sales = self.data["hist_data_city_area" + postfix]
        municipality_sales = self.data["hist_data_municipality" + postfix]
        labels = (self.data["city_area" + postfix],
                  self.data["municipality" + postfix])
        self.sales_plot = BarChart(list(city_area_sales.keys()),
                                   list(city_area_sales.values()),
                                   list(municipality_sales.keys()),
                                   list(municipality_sales.values()),
                                   getattr(self.parent.ui,
                                           prefix + "hist_data_city_area"),
                                   getattr(self.parent.ui,
                                           prefix + "hist_data_municipality"),
                                   labels, precision=-3, width=1000)

    def add_view_charts(self, prefix: str, postfix: str):
        """
        method for adding double bar chart to the statistic model

        Parameters
        ----------
        prefix      : str
                      name of prefix, i.e. "graphics"
        postfix     : str
                      index if used in naming of line_edits

        """
        original = dict(*self.data["views_development" + postfix][0].values())
        effect = dict(*self.data["views_development" + postfix][1].values())

        value = self.data["baseline" + postfix][0].values()
        lower = self.data["baseline" + postfix][1].values()
        upper = self.data["baseline" + postfix][2].values()

        self.view_plot = DoubleBarChart(list(original.keys()),
                                        list(original.values()),
                                        list(effect.keys()),
                                        list(effect.values()),
                                        getattr(self.parent.ui,
                                                prefix + "views_development"),
                                        getattr(self.parent.ui,
                                                prefix + "accumulated"))
        self.error_plot = ErrorBarPlot(y=list(value), top=list(upper), bottom=list(lower),
                                       graphics_view=getattr(self.parent.ui, prefix + "baseline"),
                                       labels="Klikk på annonsen (forventet)", units=("", " klikk"),
                                       x_time=list(original.keys()))
        self.view_plot.connect(self.error_plot, getattr(self.parent.ui, prefix + "baseline"))

    def add_statistics_label(self, key: str, postfix: str):
        """
        method for adding statistics specific labels

        Parameters
        ----------
        key         : str
                      name of label to change
        postfix     : str
                      index if used in naming of line_edits

        """
        Assertor.assert_data_types([key, postfix], [str, str])
        if key in ["city_area", "municipality"]:
            getattr(self.parent.ui, "label_" + key + "_sqm_price").setText(
                "KMP ({})".format(self.data[key + postfix]))
            getattr(self.parent.ui, "label_sales_" + key).setText(
                "Salg ({})".format(self.data[key + postfix]))
        else:
            getattr(self.parent.ui, "line_edit_" + key).setText(
                self.data[key + postfix])
