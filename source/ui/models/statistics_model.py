# -*- coding: utf-8 -*-
"""
Module of the Statistics model which handles all the statistics from the Finn Adverts

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtCore import QObject

from pandas import DataFrame

from source.ui.graphics import BarChart, DoubleBarChart, ChangeBarChart, RatioChart, \
    BarChartWithLine
from source.util import Assertor
from source.domain import Amount, Percent

from ..util import CreateHtmlTable
from .table_model import TableModel
from .model import Model


class StatisticsModel(Model):
    """
    Implementation of the Statistics model for which all the Finn based statistics logic is stored

    """
    _statistics_keys = ["finnkode", "firstpublished", "edited", "prisantydning", "fellesgjeld",
                        "totalpris", "sqm_price", "city_area_sqm_price", "municipality_sqm_price",
                        "primrrom", "bruttoareal", "views", "emails", "favorites",
                        "city_area_sqm_price", "municipality_sqm_price", "city_area",
                        "municipality", "hist_data_city_area", "hist_data_municipality",
                        "hist_data_city_area_count", "hist_data_municipality_count",
                        "age_distribution", "info", "civil_status", "education", "income",
                        "higheducation", "higheducation_location", "family_composition",
                        "age_distribution_children", "kindergardens", "kindergardens_location",
                        "schools", "schools_location", "highschools", "highschools_location",
                        "family_rating", "safety_rating", "noise_rating", "environment_rating",
                        "gardens_rating", "roads_rating", "housing_stock", "housing_ownership"]
    _ad_charts = ["hist_data_city_area", "hist_data_municipality", "ratio_statistics"]
    _community_charts = ["age_distribution_city_area", "age_distribution_city",
                         "civil_status_city_area", "civil_status_city",
                         "education_city_area", "education_city", "income_city_area",
                         "income_city", "family_composition_city_area", "family_composition_city",
                         "age_distribution_children_city_area", "age_distribution_children_city",
                         "housing_stock_city_area", "housing_stock_city",
                         "housing_ownership_city_area", "housing_ownership_city"]

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
        self.ration_plot = None
        self.age_dist_city_area_plot = None
        self.age_dist_city_plot = None
        self.civil_status_city_area_plot = None
        self.civil_status_city_plot = None
        self.education_city_area_plot = None
        self.education_city_plot = None
        self.income_city_area_plot = None
        self.income_city_plot = None
        self.family_composition_city_area_plot = None
        self.family_composition_city_plot = None
        self.age_dist_children_city_area_plot = None
        self.age_dist_children_city_plot = None
        self.families_with_children_city_area_plot = None
        self.families_with_children_city_plot = None
        self.housing_stock_city_area_plot = None
        self.housing_stock_city_plot = None
        self.housing_ownership_city_area_plot = None
        self.housing_ownership_city_plot = None

    def add_statistics_info(self, postfix: str):
        """
        method for adding statistics info to StatisticsModel

        Parameters
        ----------
        postfix     : str
                      index if used in naming of line_edits

        """
        Assertor.assert_data_types([postfix], [str])
        self.clear_charts()
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
                self.add_sqm_dist_charts(prefix, postfix, key)
            elif key == "hist_data_city_area":
                pass
            elif key == "age_distribution":
                self.add_age_dist_chart(prefix, postfix, key)
            elif key == "civil_status":
                self.add_civil_status_chart(prefix, postfix, key)
            elif key == "education":
                self.add_education_chart(prefix, postfix, key)
            elif key == "income":
                self.add_income_chart(prefix, postfix, key)
            elif key == "higheducation":
                self.add_pois_table(postfix, key)
            elif key == "higheducation_location":
                pass
            elif key == "family_composition":
                self.add_family_composition_chart(prefix, postfix, key)
            elif key == "age_distribution_children":
                self.add_age_dist_children_chart(prefix, postfix, key)
            elif key == "kindergardens":
                self.add_pois_table(postfix, key)
            elif key == "kindergardens_location":
                pass
            elif key == "schools":
                self.add_pois_table(postfix, key)
            elif key == "schools_location":
                pass
            elif key == "highschools":
                self.add_pois_table(postfix, key)
            elif key == "highschools_location":
                pass
            elif key == "family_rating":
                self.add_pois_table(postfix, key, resize=True)
            elif key == "safety_rating":
                self.add_pois_table(postfix, key, resize=True)
            elif key == "noise_rating":
                self.add_pois_table(postfix, key, resize=True)
            elif key == "environment_rating":
                self.add_pois_table(postfix, key, resize=True)
            elif key == "gardens_rating":
                self.add_pois_table(postfix, key, resize=True)
            elif key == "roads_rating":
                self.add_pois_table(postfix, key, resize=True)
            elif key == "housing_stock":
                self.add_housing_stock_chart(prefix, postfix, key)
            elif key == "housing_ownership":
                self.add_housing_ownership_chart(prefix, postfix, key)
            elif key == "info":
                self.add_map(postfix, key, university="higheducation_location",
                             kindergarden="kindergardens_location", schools="schools_location",
                             highschools="highschools_location")
            else:
                if key + postfix in self.data.keys():
                    self.add_statistics_label(key, postfix)
                else:
                    if key not in ["municipality", "city_area"]:
                        getattr(self.parent.ui, "line_edit_" + key).clear()
        self.configure_charts(prefix)

    def configure_charts(self, prefix):
        """
        method for configuring charts

        Parameters
        ----------
        prefix      : str
                      name of prefix, i.e. "graphics"

        """
        for graphics_view in self._ad_charts + self._community_charts:
            getattr(self.parent.ui, prefix + graphics_view).setMouseEnabled(x=False, y=False)
            getattr(self.parent.ui, prefix + graphics_view).getAxis('left').setStyle(
                showValues=False)
            getattr(self.parent.ui, prefix + graphics_view).getAxis('bottom').setStyle(
                showValues=False)
            getattr(self.parent.ui, prefix + graphics_view).getViewBox().enableAutoRange()
            getattr(self.parent.ui, prefix + graphics_view).setMenuEnabled(False)

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
            elif key in ["hist_data_city_area", "hist_data_municipality", "views_development",
                         "age_distribution", "civil_status", "education", "income", "higheducation",
                         "higheducation_location", "info", "family_composition",
                         "age_distribution_children", "kindergardens", "kindergardens_location",
                         "schools", "schools_location", "highschools", "highschools_location",
                         "family_rating", "safety_rating", "noise_rating", "environment_rating",
                         "gardens_rating", "roads_rating", "housing_stock", "housing_ownership"]:
                continue
            else:
                getattr(self.parent.ui, "line_edit_" + key).clear()
            self.clear_charts()

    def clear_charts(self):
        """
        method for clearing charts

        """
        BarChart.clear_graphics(self.parent.ui.graphics_view_hist_data_city_area)
        BarChart.clear_graphics(self.parent.ui.graphics_view_hist_data_municipality)
        RatioChart.clear_graphics(self.parent.ui.graphics_view_ratio_statistics)
        BarChartWithLine.clear_graphics(
            self.parent.ui.graphics_view_age_distribution_city_area,
            self.parent.ui.table_view_age_distribution)
        BarChartWithLine.clear_graphics(self.parent.ui.graphics_view_age_distribution_city,
                                        self.parent.ui.table_view_age_distribution)
        BarChartWithLine.clear_graphics(self.parent.ui.graphics_view_civil_status_city_area,
                                        self.parent.ui.table_view_civil_status)
        BarChartWithLine.clear_graphics(self.parent.ui.graphics_view_civil_status_city,
                                        self.parent.ui.table_view_civil_status)
        BarChartWithLine.clear_graphics(self.parent.ui.graphics_view_education_city_area,
                                        self.parent.ui.table_view_education)
        BarChartWithLine.clear_graphics(self.parent.ui.graphics_view_education_city,
                                        self.parent.ui.table_view_education)
        BarChartWithLine.clear_graphics(self.parent.ui.graphics_view_income_city_area,
                                        self.parent.ui.table_view_income)
        BarChartWithLine.clear_graphics(self.parent.ui.graphics_view_income_city,
                                        self.parent.ui.table_view_income)

        self.parent.ui.table_view_higheducation.setModel(None)
        self.parent.ui.table_view_higheducation.clearSpans()
        self.parent.ui.table_view_kindergardens.setModel(None)
        self.parent.ui.table_view_kindergardens.clearSpans()
        self.parent.map_view.web_view_map.close()

        BarChartWithLine.clear_graphics(self.parent.ui.graphics_view_family_composition_city_area,
                                        self.parent.ui.table_view_family_composition)
        BarChartWithLine.clear_graphics(self.parent.ui.graphics_view_family_composition_city,
                                        self.parent.ui.table_view_family_composition)
        BarChartWithLine.clear_graphics(
            self.parent.ui.graphics_view_age_distribution_children_city_area,
            self.parent.ui.table_view_age_distribution_children)
        BarChartWithLine.clear_graphics(self.parent.ui.graphics_view_age_distribution_children_city,
                                        self.parent.ui.table_view_age_distribution_children)
        BarChartWithLine.clear_graphics(self.parent.ui.graphics_view_housing_stock_city_area,
                                        self.parent.ui.table_view_housing_stock)
        BarChartWithLine.clear_graphics(self.parent.ui.graphics_view_housing_stock_city,
                                        self.parent.ui.table_view_housing_stock)
        BarChartWithLine.clear_graphics(self.parent.ui.graphics_view_housing_ownership_city_area,
                                        self.parent.ui.table_view_housing_ownership)
        BarChartWithLine.clear_graphics(self.parent.ui.graphics_view_housing_ownership_city,
                                        self.parent.ui.table_view_housing_ownership)

    def add_sqm_dist_charts(self, prefix: str, postfix: str, key: str):
        """
        method for adding square meter distribution chart to the statistics model

        Parameters
        ----------
        prefix      : str
                      name of prefix, i.e. "graphics"
        postfix     : str
                      index if used in naming of line_edits
        key         : str
                      name of label to change

        """
        Assertor.assert_data_types([prefix, postfix], [str, str])
        BarChart.clear_graphics(
            getattr(self.parent.ui, prefix + "hist_data_municipality"))
        BarChart.clear_graphics(getattr(self.parent.ui, prefix + "hist_data_city_area"))
        RatioChart.clear_graphics(self.parent.ui.graphics_view_ratio_statistics)
        if key + postfix in self.data.keys() and self.data[key + postfix]:
            if sum(list(self.data["hist_data_city_area" + postfix].values())) != 0:
                city_area_sales = self.data["hist_data_city_area" + postfix]
                municipality_sales = self.data["hist_data_municipality" + postfix]

                if "city_area" + postfix in self.data.keys() and \
                        "municipality" + postfix in self.data.keys():
                    labels = (self.data["city_area" + postfix], self.data["municipality" + postfix])
                elif "city_area" + postfix in self.data.keys():
                    labels = (self.data["city_area" + postfix], "")
                elif "municipality" + postfix in self.data.keys():
                    labels = ("", self.data["municipality" + postfix])
                else:
                    labels = ("", "")

                self.sales_plot = BarChart(list(city_area_sales.keys()),
                                           list(city_area_sales.values()),
                                           list(municipality_sales.keys()),
                                           list(municipality_sales.values()),
                                           getattr(self.parent.ui,
                                                   prefix + "hist_data_city_area"),
                                           getattr(self.parent.ui,
                                                   prefix + "hist_data_municipality"),
                                           labels, units=(" kr/m²", " salg", " kr/m²", " salg"),
                                           precision=-3, width=1000,
                                           average=self.data["sqm_price" + postfix].replace(
                                               " ", "").replace("kr/m²", ""))
                self.ration_plot = RatioChart(list(municipality_sales.keys()),
                                              list(city_area_sales.values()),
                                              list(municipality_sales.values()),
                                              getattr(self.parent.ui, prefix + "ratio_statistics"),
                                              "Forhold ({})".format(" / ".join(labels)),
                                              units=(" kr/m²", ""), precision=-3, width=1000)
                self.sales_plot.connect(self.ration_plot,
                                        self.parent.ui.graphics_view_ratio_statistics)

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
        dates = list(self.data["views_development" + postfix]["dates"].values())
        total = list(self.data["views_development" + postfix]["total_views"].values())
        organic = list(self.data["views_development" + postfix]["organic_views"].values())
        change = list(self.data["views_development" + postfix]["change"].values())
        accumulated = list(self.data["views_development" + postfix]["accumulated"].values())

        self.view_plot = DoubleBarChart(dates, total, dates, organic, dates, accumulated,
                                        getattr(self.parent.ui, prefix + "views_development"),
                                        getattr(self.parent.ui, prefix + "accumulated"),
                                        ("Klikk på annonsen (per dag)",
                                         "Klikk på annonsen (akkumulert)"),
                                        ("", " klikk", "", " klikk"))
        self.change_plot = ChangeBarChart(dates, change, getattr(self.parent.ui, prefix + "change"),
                                          labels="Klikk på annonsen (endring dag-til-dag)",
                                          units=("", " %"), x_labels=dates)
        self.view_plot.connect(self.change_plot, getattr(self.parent.ui, prefix + "change"))

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

    def add_dist_chart(self, prefix: str, postfix: str, key: str, plot_name_1: str,
                       plot_name_2: str, table_name: str, dist_name: str, dist_var_1: str,
                       dist_var_2: str, ignore_total: bool = True):
        """
        method for adding distribution chart to the statistics model

        Parameters
        ----------
        prefix      : str
                      name of prefix, i.e. "graphics"
        postfix     : str
                      index if used in naming of line_edits
        key         : str
                      name of label to change
        plot_name_1 : str
                      name of first plot
        plot_name_2 : str
                      name of second plot
        table_name  : str
                      name of table
        dist_name   : str
                      name of distribution variable
        dist_var_1  : str
                      name of instance variable for distribution
        dist_var_2  : str
                      name of second instance variable for distribution
        ignore_total: str
                      boolean for handling total values

        """
        Assertor.assert_data_types([prefix, postfix, key, plot_name_1, plot_name_2, table_name,
                                    dist_name, dist_var_1, dist_var_2, ignore_total],
                                   [str, str, str, str, str, str, str, str, str, bool])
        BarChart.clear_graphics(
            getattr(self.parent.ui, prefix + plot_name_1))
        BarChart.clear_graphics(getattr(self.parent.ui, prefix + plot_name_2))
        if key + postfix in self.data.keys() and self.data[key + postfix]:
            dist = self.data[key + postfix]
            city_area_dist = dist["Nabolag"][:-2] if ignore_total else dist["Nabolag"]
            city_dist = dist["By"][:-2] if ignore_total else dist["By"]
            dist_range = list(range(len(city_area_dist)))
            if "info" + postfix in self.data.keys():
                if self.data["info" + postfix]["neighborhood"]:
                    neighbourhood = self.data["info" + postfix]["neighborhood"]["name"] \
                        .replace("-", " - ")
                    city = self.data["info" + postfix]["neighborhood"]["city"]
                else:
                    neighbourhood = self.data["info" + postfix]["census"].replace("-", " - ")
                    city = self.data["info" + postfix]["city"].replace("-", " - ")
            else:
                neighbourhood = ""
                city = ""

            if "city_area" + postfix in self.data.keys():
                city_area = self.data["city_area" + postfix]
            else:
                city_area = ""

            if sum(city_area_dist) != 0:
                dist_df = {"Gruppe": [],
                           "Nabolag": [],
                           "By": []}
                for keys, values in dist.items():
                    if keys == "Gruppe":
                        dist_df[keys] = values
                    else:
                        if ignore_total:
                            dist_df[keys] = [Percent(str(val / 100)).value if i not in (
                                len(values) - 1, len(values) - 2) else Amount(str(val)).amount
                                             for i, val in enumerate(values)]
                        else:
                            dist_df[keys] = [Percent(str(val / 100)).value for i, val in
                                             enumerate(values)]

                table_model = TableModel(DataFrame(dist_df))
                getattr(self.parent.ui, table_name).setModel(table_model)
                getattr(self.parent.ui, table_name).horizontalHeader().setSectionResizeMode(
                    QHeaderView.Stretch)

                setattr(self, dist_var_1, BarChartWithLine(
                    dist_range, city_area_dist,
                    getattr(self.parent.ui, prefix + plot_name_1),
                    getattr(self.parent.ui, table_name),
                    width=0.5, reverse=False,
                    legend='<div style="text-align: center">'
                           '<span style="font-size: 10pt">{}:</span><br>'
                           '<span style="font-size: 10pt">{}</span><br>'
                           '<span style="font-size: 10pt">({})</span><br>'
                           '</div>'.format(dist_name, neighbourhood, city_area)))

                setattr(self, dist_var_2, BarChartWithLine(
                    dist_range, city_dist,
                    getattr(self.parent.ui, prefix + plot_name_2),
                    getattr(self.parent.ui, table_name),
                    width=0.5, reverse=False,
                    legend='<div style="text-align: center">'
                           '<span style="font-size: 10pt">{}:</span><br>'
                           '<span style="font-size: 10pt">{}</span><br>'
                           '</div>'.format(dist_name, city)))

                getattr(self, dist_var_1).table_view_mapping()
                getattr(self, dist_var_2).table_view_mapping()

    def add_age_dist_chart(self, prefix: str, postfix: str, key: str):
        """
        method for adding age distribution chart to the statistics model

        Parameters
        ----------
        prefix      : str
                      name of prefix, i.e. "graphics"
        postfix     : str
                      index if used in naming of line_edits
        key         : str
                      name of label to change

        """
        self.add_dist_chart(prefix, postfix, key, "age_distribution_city_area",
                            "age_distribution_city", "table_view_age_distribution",
                            "Aldersfordeling", "age_dist_city_area_plot", "age_dist_city_plot")

    def add_civil_status_chart(self, prefix: str, postfix: str, key: str):
        """
        method for adding civil_status distribution chart to the statistics model

        Parameters
        ----------
        prefix      : str
                      name of prefix, i.e. "graphics"
        postfix     : str
                      index if used in naming of line_edits
        key         : str
                      name of label to change

        """
        self.add_dist_chart(prefix, postfix, key, "civil_status_city_area",
                            "civil_status_city", "table_view_civil_status",
                            "Sivil status fordeling", "civil_status_city_area_plot",
                            "civil_status_city_plot", ignore_total=False)

    def add_education_chart(self, prefix: str, postfix: str, key: str):
        """
        method for adding education distribution chart to the statistics model

        Parameters
        ----------
        prefix      : str
                      name of prefix, i.e. "graphics"
        postfix     : str
                      index if used in naming of line_edits
        key         : str
                      name of label to change

        """
        self.add_dist_chart(prefix, postfix, key, "education_city_area",
                            "education_city", "table_view_education",
                            "Utdanningsfordeling", "education_city_area_plot",
                            "education_city_plot", ignore_total=False)

    def add_income_chart(self, prefix: str, postfix: str, key: str):
        """
        method for adding income distribution chart to the statistics model

        Parameters
        ----------
        prefix      : str
                      name of prefix, i.e. "graphics"
        postfix     : str
                      index if used in naming of line_edits
        key         : str
                      name of label to change

        """
        self.add_dist_chart(prefix, postfix, key, "income_city_area", "income_city",
                            "table_view_income", "Inntektsfordeling", "income_city_area_plot",
                            "income_city_plot", ignore_total=False)

    def add_pois_table(self, postfix: str, key: str, resize=False):
        """
        method for adding pois table

        Parameters
        ----------
        postfix     : str
                      index if used in naming of line_edits
        key         : str
                      name of label to change
        resize      : bool
                      boolean for widths in table to content

        """
        getattr(self.parent.ui, "table_view_" + key).setModel(None)
        if key + postfix in self.data.keys() and self.data[key + postfix]:
            pois_table_model = TableModel(DataFrame(self.data[key + postfix]))
            getattr(self.parent.ui, "table_view_" + key).setModel(pois_table_model)

            if resize:
                getattr(self.parent.ui, "table_view_" + key).verticalHeader().setSectionResizeMode(
                    QHeaderView.ResizeToContents)
                getattr(self.parent.ui,
                        "table_view_" + key).horizontalHeader().setSectionResizeMode(
                    0, QHeaderView.Stretch)
                getattr(self.parent.ui,
                        "table_view_" + key).horizontalHeader().setSectionResizeMode(
                    1, QHeaderView.ResizeToContents)
                getattr(self.parent.ui,
                        "table_view_" + key).horizontalHeader().setSectionResizeMode(
                    2, QHeaderView.ResizeToContents)
                getattr(self.parent.ui, "table_view_" + key).setWordWrap(False)
            else:
                getattr(self.parent.ui,
                        "table_view_" + key).horizontalHeader().setSectionResizeMode(
                    0, QHeaderView.Fixed)
                getattr(self.parent.ui, "table_view_" + key).setColumnWidth(0, 180)
                getattr(self.parent.ui,
                        "table_view_" + key).horizontalHeader().setSectionResizeMode(
                    1, QHeaderView.Fixed)
                getattr(self.parent.ui, "table_view_" + key).setColumnWidth(1, 65)
                getattr(self.parent.ui,
                        "table_view_" + key).horizontalHeader().setSectionResizeMode(
                    2, QHeaderView.Fixed)
                getattr(self.parent.ui, "table_view_" + key).setColumnWidth(2, 65)
                getattr(self.parent.ui, "table_view_" + key).verticalHeader().setSectionResizeMode(
                    QHeaderView.ResizeToContents)
                getattr(self.parent.ui, "table_view_" + key).setWordWrap(True)

    def add_map(self, postfix: str, keys: str, university: str, kindergarden: str, schools: str,
                highschools: str):
        """
        method for adding pois table

        Parameters
        ----------
        postfix       : str
                        index if used in naming of line_edits
        keys          : str
                        name of label to change
        university    : str
                        name of university data dict
        kindergarden  : str
                        name of kindergarden data dict
        schools       : str
                        name of schools data dict
        highschools   : str
                        name of highschools data dict

        """
        self.parent.map_view.web_view_map.close()
        if keys + postfix in self.data.keys() and self.data[keys + postfix]:
            lat = self.data[keys + postfix]["location"]["lat"]
            long = self.data[keys + postfix]["location"]["long"]
            html_table = CreateHtmlTable(self.data["info" + postfix])

            self.parent.map_view.web_view_map.page().settings().setAttribute(
                QWebEngineSettings.ShowScrollBars, False)
            self.parent.map_view.map_model \
                .show_map(coords=[lat, long],
                          web_engine_view=self.parent.map_view.web_view_map,
                          pop_up=html_table.html_table(),
                          university=self.data[university + postfix]
                          if university + postfix in self.data.keys() else "",
                          kindergarden=self.data[kindergarden + postfix]
                          if kindergarden + postfix in self.data.keys() else "",
                          schools=self.data[schools + postfix]
                          if kindergarden + postfix in self.data.keys() else "",
                          highschools=self.data[highschools + postfix]
                          if highschools + postfix in self.data.keys() else "")

    def add_family_composition_chart(self, prefix: str, postfix: str, key: str):
        """
        method for adding family composition chart to the statistics model

        Parameters
        ----------
        prefix      : str
                      name of prefix, i.e. "graphics"
        postfix     : str
                      index if used in naming of line_edits
        key         : str
                      name of label to change

        """
        self.add_dist_chart(prefix, postfix, key, "family_composition_city_area",
                            "family_composition_city", "table_view_family_composition",
                            "Familiefordeling", "family_composition_city_area_plot",
                            "family_composition_city_plot", ignore_total=False)

    def add_age_dist_children_chart(self, prefix, postfix, key):
        """
        method for adding age distribution children chart to the statistics model

        Parameters
        ----------
        prefix      : str
                      name of prefix, i.e. "graphics"
        postfix     : str
                      index if used in naming of line_edits
        key         : str
                      name of label to change

        """
        self.add_dist_chart(prefix, postfix, key, "age_distribution_children_city_area",
                            "age_distribution_children_city",
                            "table_view_age_distribution_children", "Aldersfordeling barn",
                            "age_distribution_children_city_area_plot",
                            "age_distribution_children_city_plot", ignore_total=False)

    def add_housing_stock_chart(self, prefix, postfix, key):
        """
        method for adding housing stock chart to the statistics model

        Parameters
        ----------
        prefix      : str
                      name of prefix, i.e. "graphics"
        postfix     : str
                      index if used in naming of line_edits
        key         : str
                      name of label to change

        """
        self.add_dist_chart(prefix, postfix, key, "housing_stock_city_area", "housing_stock_city",
                            "table_view_housing_stock", "Boligmasse",
                            "housing_stock_city_area_plot", "housing_stock_city_plot",
                            ignore_total=False)

    def add_housing_ownership_chart(self, prefix, postfix, key):
        """
        method for adding housing stock chart to the statistics model

        Parameters
        ----------
        prefix      : str
                      name of prefix, i.e. "graphics"
        postfix     : str
                      index if used in naming of line_edits
        key         : str
                      name of label to change

        """
        self.add_dist_chart(prefix, postfix, key, "housing_ownership_city_area",
                            "housing_ownership_city", "table_view_housing_ownership",
                            "Bolig eierskap", "housing_ownership_city_area_plot",
                            "housing_ownership_city_plot", ignore_total=False)
