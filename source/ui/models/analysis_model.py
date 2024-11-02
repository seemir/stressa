# -*- coding: utf-8 -*-
"""
Model with Analysis logic of mortgages

"""
__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pandas as pd

from PyQt5.QtWidgets import QHeaderView  # pylint: disable=no-name-in-module
from PyQt5.QtCore import QObject, Qt  # pylint: disable=no-name-in-module

from source.app import MortgageAnalysisProcess
from source.domain import Mortgage
from source.util import Assertor

from .table_model import TableModel
from .model import Model

from ..graphics import StackedBarChartWithLine


class AnalysisModel(Model):
    """
    Implementation of the Analysis model for which mortgages are analysed

    """

    _analysis_keys = ['arsinntekt_aar', 'belaning', 'belaningsgrad',
                      'egenkapital_2', 'egenkapital_andel', 'betjeningsevne_2', 'total_ramme',
                      'krav_belaning', 'krav_egenkapital_andel', 'krav_belaningsgrad',
                      'krav_total_ramme', 'krav_egenkapital', 'stresstest_annuitet',
                      'stresstest_serie', 'krav_stresstest_annuitet', 'krav_stresstest_serie',
                      'krav_betjeningsevne', 'laan_annuitet', 'total_rente_annuitet',
                      'total_belop_annuitet', 'laan_serie', 'total_rente_serie',
                      'total_belop_serie', 'laan_andel_annuitet', 'total_rente_andel_annuitet',
                      'total_belop_andel_annuitet', 'laan_andel_serie',
                      'total_rente_andel_serie', 'total_belop_andel_serie',
                      'snitt_total_termin_belop_annitet']

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

        self.parent.ui_form.push_button_analyse.clicked.connect(
            self.analyze_mortgage)
        self.bar_plot_annuitet_total = None
        self.bar_plot_serie_total = None
        self.bar_plot_annuitet_period = None
        self.bar_plot_serie_period = None

    @property
    def analysis_keys(self):
        """
        analysis keys getter

        """
        return self._analysis_keys

    def analyze_mortgage(self):
        """
        method for analyze mortgage

        """
        self.data.update(self.parent.budget_model.data)
        self.data.update(self.parent.mortgage_model.data)
        self.data.update(self.parent.home_model.data)

        if all(element in self.data for element in
               Mortgage.requirements_mortgage):
            self.parent.restructure_model.clear_all()
            self.parent.payment_model.clear_all()

            self.parent.ui_form.tab_widget_home.setCurrentIndex(1)

            mortgage_analysis_data = MortgageAnalysisProcess(
                self.data).mortgage()
            self.set_line_edits(line_edit_text='',
                                line_edits=self.analysis_keys,
                                data=mortgage_analysis_data)

            payment_values_annuitet_total, payment_values_annuitet_period = \
                self.fixed_mortgage_display(mortgage_analysis_data)
            self.series_mortgage_display(mortgage_analysis_data,
                                         payment_values_annuitet_total,
                                         payment_values_annuitet_period)

            self.configure_charts()

            payment_keys = ["start_dato_annuitet", "slutt_dato_annuitet",
                            "total_termin_annuitet",
                            "aar_annuitet", "termin_aar_annuitet",
                            "laan_annuitet",
                            "rente_annuitet", "total_rente_annuitet",
                            "total_belop_annuitet",
                            "start_dato_serie", "nedbetalingsplan_annuitet",
                            "slutt_dato_serie",
                            "total_termin_serie", "aar_serie",
                            "termin_aar_serie", "laan_serie",
                            "rente_serie", "total_rente_serie",
                            "total_belop_serie",
                            "nedbetalingsplan_serie",
                            "betjeningsevne_plan_serie",
                            "betjeningsevne_mnd_serie",
                            "betjeningsevne_plan_annuitet",
                            "betjeningsevne_mnd_annuitet"]

            for payment_key in payment_keys:
                if payment_key in mortgage_analysis_data.keys():
                    self.data.update(
                        {payment_key: mortgage_analysis_data[payment_key]})

    def fixed_mortgage_display(self, mortgage_analysis_data: dict):
        """
        method for displaying annuitet mortgage information

        """

        payment_values_annuitet_total = []
        payment_values_annuitet_period = []

        if "nedbetalingsplan_annuitet_overview" in mortgage_analysis_data.keys():
            StackedBarChartWithLine.clear_graphics(
                self.parent.ui_form.graphics_view_annuitet_overview,
                self.parent.ui_form.table_view_annuitet_overview)

            StackedBarChartWithLine.clear_graphics(
                self.parent.ui_form.graphics_view_annuitet_period,
                self.parent.ui_form.table_view_annuitet_overview)

            payment_data_model_fixed = TableModel(
                pd.DataFrame(mortgage_analysis_data[
                                 "nedbetalingsplan_annuitet_overview"]),
                alignment=Qt.AlignCenter)
            self.parent.ui_form.table_view_annuitet_overview.setModel(
                payment_data_model_fixed)

            termin = list(
                mortgage_analysis_data["nedbetalingsplan_annuitet_overview"][
                    "År"].values())[
                     ::-1]
            principal_total = list(
                mortgage_analysis_data["nedbetalingsplan_annuitet_overview"][
                    "Avdrag.total"].values())[::-1]
            payment_total = list(
                mortgage_analysis_data["nedbetalingsplan_annuitet_overview"][
                    "T.beløp.total"].values())[::-1]

            principal_values_total = [
                int(val.replace("kr", "").replace(" ", "").replace("\xa0", ""))
                for val in principal_total]
            payment_values_annuitet_total = [
                int(val.replace("kr", "").replace(" ", "").replace("\xa0", ""))
                for val in payment_total]

            self.bar_plot_annuitet_total = StackedBarChartWithLine(
                termin, payment_values_annuitet_total, principal_values_total,
                self.parent.ui_form.graphics_view_annuitet_overview,
                self.parent.ui_form.table_view_annuitet_overview,
                y_max=int(max(payment_values_annuitet_total) * 1.33))

            self.bar_plot_annuitet_total.table_view_mapping()

            principal_period = list(
                mortgage_analysis_data["nedbetalingsplan_annuitet_overview"][
                    "Avdrag"].values())[::-1]
            payment_period = list(
                mortgage_analysis_data["nedbetalingsplan_annuitet_overview"][
                    "T.beløp"].values())[::-1]

            principal_values_period = [
                int(val.replace("kr", "").replace(" ", "").replace("\xa0", ""))
                for val in principal_period]
            payment_values_annuitet_period = [
                int(val.replace("kr", "").replace(" ", "").replace("\xa0", ""))
                for val in payment_period]

            self.bar_plot_annuitet_period = StackedBarChartWithLine(
                termin, payment_values_annuitet_period, principal_values_period,
                self.parent.ui_form.graphics_view_annuitet_period,
                self.parent.ui_form.table_view_annuitet_overview,
                y_max=int(max(payment_values_annuitet_period) * 1.33))

            self.bar_plot_annuitet_period.table_view_mapping()

        return payment_values_annuitet_total, payment_values_annuitet_period

    def series_mortgage_display(self, mortgage_analysis_data: dict,
                                payment_values_annuitet_total: list,
                                payment_values_annuitet_period: list):
        """
        method for displaying series mortgage data

        """
        if "nedbetalingsplan_serie_overview" in mortgage_analysis_data.keys():
            StackedBarChartWithLine.clear_graphics(
                self.parent.ui_form.graphics_view_serie_overview,
                self.parent.ui_form.table_view_serie_overview)

            StackedBarChartWithLine.clear_graphics(
                self.parent.ui_form.graphics_view_serie_period,
                self.parent.ui_form.table_view_serie_overview)

            payment_data_model_fixed = TableModel(
                pd.DataFrame(
                    mortgage_analysis_data["nedbetalingsplan_serie_overview"]),
                alignment=Qt.AlignCenter)
            self.parent.ui_form.table_view_serie_overview.setModel(
                payment_data_model_fixed)

            termin = list(
                mortgage_analysis_data["nedbetalingsplan_serie_overview"][
                    "År"].values())[
                     ::-1]
            principal_total = list(
                mortgage_analysis_data["nedbetalingsplan_serie_overview"][
                    "Avdrag.total"].values())[::-1]
            payment_total = list(
                mortgage_analysis_data["nedbetalingsplan_serie_overview"][
                    "T.beløp.total"].values())[::-1]

            principal_values_total = [
                int(val.replace("kr", "").replace(" ", "").replace("\xa0", ""))
                for val in principal_total]
            payment_values_serie_total = [
                int(val.replace("kr", "").replace(" ", "").replace("\xa0", ""))
                for val in payment_total]

            self.bar_plot_serie_total = StackedBarChartWithLine(
                termin, payment_values_serie_total, principal_values_total,
                self.parent.ui_form.graphics_view_serie_overview,
                self.parent.ui_form.table_view_serie_overview,
                y_max=int(max(payment_values_annuitet_total) * 1.33))

            self.bar_plot_serie_total.table_view_mapping()

            principal_period = list(
                mortgage_analysis_data["nedbetalingsplan_serie_overview"][
                    "Avdrag"].values())[::-1]
            payment_period = list(
                mortgage_analysis_data["nedbetalingsplan_serie_overview"][
                    "T.beløp"].values())[::-1]

            principal_values_period = [
                int(val.replace("kr", "").replace(" ", "").replace("\xa0", ""))
                for val in principal_period]
            payment_values_serie_period = [
                int(val.replace("kr", "").replace(" ", "").replace("\xa0", ""))
                for val in payment_period]

            self.bar_plot_serie_period = StackedBarChartWithLine(
                termin, payment_values_serie_period, principal_values_period,
                self.parent.ui_form.graphics_view_serie_period,
                self.parent.ui_form.table_view_serie_overview,
                y_max=int(max(payment_values_annuitet_period) * 1.33))

            self.bar_plot_serie_period.table_view_mapping()

    def configure_charts(self):
        """
        method for configuring charts

        """
        self.parent.ui_form.table_view_annuitet_overview.horizontalHeader() \
            .setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.parent.ui_form.table_view_annuitet_overview.horizontalHeader() \
            .setSectionResizeMode(1, QHeaderView.Stretch)
        self.parent.ui_form.table_view_annuitet_overview.horizontalHeader() \
            .setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.parent.ui_form.table_view_annuitet_overview.horizontalHeader() \
            .setSectionResizeMode(3, QHeaderView.Stretch)
        self.parent.ui_form.table_view_annuitet_overview.horizontalHeader() \
            .setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.parent.ui_form.table_view_annuitet_overview.horizontalHeader() \
            .setSectionResizeMode(5, QHeaderView.Stretch)
        self.parent.ui_form.table_view_annuitet_overview.horizontalHeader() \
            .setSectionResizeMode(6, QHeaderView.ResizeToContents)

        self.parent.ui_form.table_view_serie_overview.horizontalHeader() \
            .setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.parent.ui_form.table_view_serie_overview.horizontalHeader() \
            .setSectionResizeMode(1, QHeaderView.Stretch)
        self.parent.ui_form.table_view_serie_overview.horizontalHeader() \
            .setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.parent.ui_form.table_view_serie_overview.horizontalHeader() \
            .setSectionResizeMode(3, QHeaderView.Stretch)
        self.parent.ui_form.table_view_serie_overview.horizontalHeader() \
            .setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.parent.ui_form.table_view_serie_overview.horizontalHeader() \
            .setSectionResizeMode(5, QHeaderView.Stretch)
        self.parent.ui_form.table_view_serie_overview.horizontalHeader() \
            .setSectionResizeMode(6, QHeaderView.ResizeToContents)

        self.config_plots()

    def config_plots(self):
        """
        method for configure data plots

        """
        for graphics_view in ['graphics_view_annuitet_overview',
                              'graphics_view_serie_overview',
                              'graphics_view_annuitet_period',
                              'graphics_view_serie_period']:
            getattr(self.parent.ui_form, graphics_view).setMouseEnabled(x=False,
                                                                        y=False)
            getattr(self.parent.ui_form, graphics_view).getAxis(
                'left').setStyle(
                showValues=False)
            getattr(self.parent.ui_form, graphics_view).getAxis(
                'bottom').setStyle(
                showValues=False)
            getattr(self.parent.ui_form, graphics_view).hideButtons()
            getattr(self.parent.ui_form, graphics_view).setMenuEnabled(False)
            getattr(self.parent.ui_form, graphics_view).showGrid(x=True, y=True)

    def clear_all(self):
        """
        method for clearing model

        """
        StackedBarChartWithLine.clear_graphics(
            self.parent.ui_form.graphics_view_annuitet_overview,
            self.parent.ui_form.table_view_annuitet_overview)
        StackedBarChartWithLine.clear_graphics(
            self.parent.ui_form.graphics_view_serie_overview,
            self.parent.ui_form.table_view_serie_overview)

        StackedBarChartWithLine.clear_graphics(
            self.parent.ui_form.graphics_view_annuitet_period,
            self.parent.ui_form.table_view_annuitet_overview)
        StackedBarChartWithLine.clear_graphics(
            self.parent.ui_form.graphics_view_serie_period,
            self.parent.ui_form.table_view_serie_overview)

        self.data = {}
        self.clear_line_edits(self.analysis_keys)
