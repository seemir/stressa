# -*- coding: utf-8 -*-

"""
Module for main restructure model for the HomeView

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pandas as pd

from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtCore import QObject, pyqtSlot, Qt

from source.domain import Money, Mortgage, Percentage
from source.app import RestructureProcess
from source.util import Assertor

from .table_model import TableModel
from .model import Model

from ..graphics import StackedBarChartWithLine


class RestructureModel(Model):
    """
    Implementation of restructure Model in the HomeView, i.e. contains logic / mortgage
    related data inputted in the HomeView

    """
    _lanetype = ["", "Sammenligning", "Annuitetslån", "Serielån"]
    _laneperiode = [""] + [str(yr) + " år" for yr in range(1, 31)]
    _intervall = ["", "Årlig", "Halvårlig", "Kvartalsvis", "Annenhver måned", "Månedlig",
                  "Semi-månedlig", "Annenhver uke", "Ukentlig"]

    def __init__(self, parent: QObject):
        """
        Constructor / Instantiation of class

        Parameters
        ----------
        parent  : QObject
                  parent view for which the model resides

        """
        Assertor.assert_data_types([parent], [QObject])
        super().__init__(parent)

        self.parent.ui_form.combo_box_lanetype.addItems(self._lanetype)
        self.parent.ui_form.combo_box_laneperiode.addItems(self._laneperiode)
        self.parent.ui_form.combo_box_intervall.addItems(self._intervall)
        self.bar_plot_annuitet_total = None
        self.bar_plot_serie_total = None
        self.bar_plot_annuitet_period = None
        self.bar_plot_serie_period = None

    @pyqtSlot()
    def restructure_info(self):
        """
        Method for retrieving and formatting all inputted restructured information

        """
        self.parent.ui_form.combo_box_lanetype.activated.connect(
            lambda: self.set_combo_box("lanetype"))
        self.parent.ui_form.combo_box_intervall.activated.connect(
            lambda: self.set_combo_box("intervall"))
        self.parent.ui_form.combo_box_laneperiode.activated.connect(
            lambda: self.set_combo_box("laneperiode"))
        self.parent.ui_form.date_edit_startdato.editingFinished.connect(
            lambda: self.set_date_edit("startdato"))
        self.parent.ui_form.line_edit_egenkapital.textEdited.connect(
            lambda: self.set_line_edit("egenkapital", Money, "value"))
        self.parent.ui_form.line_edit_belaning.textEdited.connect(
            lambda: self.set_line_edit("belaning", Money, "value"))
        self.parent.ui_form.line_edit_nominell_rente.textEdited.connect(
            lambda: self.set_line_edit("nominell_rente", Percentage, "percentage_value"))

    def export(self):
        """
        method for analyze mortgage

        """
        restructure_data = {}
        restructure_data.update(self.parent.parent.analysis_model.data)
        restructure_data.update(self.data)
        if all(element in restructure_data.keys() for element in Mortgage.requirements_restructure):
            restructure_data = RestructureProcess(restructure_data).restructure()
            analysis_model = self.parent.parent.analysis_model

            analysis_model.set_line_edits(line_edit_text='',
                                          line_edits=analysis_model.analysis_keys,
                                          data=restructure_data)

            if "nedbetalingsplan_annuitet_overview" in restructure_data.keys():
                StackedBarChartWithLine.clear_graphics(
                    self.parent.parent.ui_form.graphics_view_annuitet_overview,
                    self.parent.parent.ui_form.table_view_annuitet_overview)

                StackedBarChartWithLine.clear_graphics(
                    self.parent.parent.ui_form.graphics_view_annuitet_period,
                    self.parent.parent.ui_form.table_view_annuitet_overview)

                payment_data_model_fixed = TableModel(
                    pd.DataFrame(restructure_data["nedbetalingsplan_annuitet_overview"]),
                    alignment=Qt.AlignCenter)
                self.parent.parent.ui_form.table_view_annuitet_overview.setModel(
                    payment_data_model_fixed)

                termin = list(
                    restructure_data["nedbetalingsplan_annuitet_overview"]["År"].values())[
                         ::-1]
                principal = list(restructure_data["nedbetalingsplan_annuitet_overview"][
                                     "Avdrag.total"].values())[::-1]
                payment = list(restructure_data["nedbetalingsplan_annuitet_overview"][
                                   "T.beløp.total"].values())[::-1]

                principal_values = [int(val.replace("kr", "").replace(" ", "").replace("\xa0", ""))
                                    for val in principal]
                payment_values_annuitet = [
                    int(val.replace("kr", "").replace(" ", "").replace("\xa0", ""))
                    for val in payment]

                self.bar_plot_annuitet_total = StackedBarChartWithLine(
                    termin, payment_values_annuitet, principal_values,
                    self.parent.parent.ui_form.graphics_view_annuitet_overview,
                    self.parent.parent.ui_form.table_view_annuitet_overview,
                    y_max=int(max(payment_values_annuitet) * 1.33))

                self.bar_plot_annuitet_total.table_view_mapping()

                principal_period = list(
                    restructure_data["nedbetalingsplan_annuitet_overview"][
                        "Avdrag"].values())[::-1]
                payment_period = list(restructure_data["nedbetalingsplan_annuitet_overview"][
                                          "T.beløp"].values())[::-1]

                principal_values_period = [
                    int(val.replace("kr", "").replace(" ", "").replace("\xa0", ""))
                    for val in principal_period]
                payment_values_annuitet_period = [
                    int(val.replace("kr", "").replace(" ", "").replace("\xa0", ""))
                    for val in payment_period]

                self.bar_plot_annuitet_period = StackedBarChartWithLine(
                    termin, payment_values_annuitet_period, principal_values_period,
                    self.parent.parent.ui_form.graphics_view_annuitet_period,
                    self.parent.parent.ui_form.table_view_annuitet_overview,
                    y_max=int(max(payment_values_annuitet_period) * 1.33))

                self.bar_plot_annuitet_period.table_view_mapping()

            if "nedbetalingsplan_serie_overview" in restructure_data.keys():
                StackedBarChartWithLine.clear_graphics(
                    self.parent.parent.ui_form.graphics_view_serie_overview,
                    self.parent.parent.ui_form.table_view_serie_overview)

                StackedBarChartWithLine.clear_graphics(
                    self.parent.parent.ui_form.graphics_view_serie_period,
                    self.parent.parent.ui_form.table_view_serie_overview)

                payment_data_model_serie = TableModel(
                    pd.DataFrame(restructure_data["nedbetalingsplan_serie_overview"]),
                    alignment=Qt.AlignCenter)
                self.parent.parent.ui_form.table_view_serie_overview.setModel(
                    payment_data_model_serie)

                termin = list(
                    restructure_data["nedbetalingsplan_serie_overview"]["År"].values())[
                         ::-1]
                principal = list(restructure_data["nedbetalingsplan_serie_overview"][
                                     "Avdrag.total"].values())[::-1]
                payment = list(restructure_data["nedbetalingsplan_serie_overview"][
                                   "T.beløp.total"].values())[::-1]

                principal_values = [int(val.replace("kr", "").replace(" ", "").replace("\xa0", ""))
                                    for val in principal]
                payment_values_serie = [
                    int(val.replace("kr", "").replace(" ", "").replace("\xa0", ""))
                    for val in payment]

                self.bar_plot_serie_total = StackedBarChartWithLine(
                    termin, payment_values_serie, principal_values,
                    self.parent.parent.ui_form.graphics_view_serie_overview,
                    self.parent.parent.ui_form.table_view_serie_overview,
                    y_max=int(max(payment_values_annuitet) * 1.33))

                self.bar_plot_serie_total.table_view_mapping()

                principal_period = list(
                    restructure_data["nedbetalingsplan_serie_overview"][
                        "Avdrag"].values())[::-1]
                payment_period = list(restructure_data["nedbetalingsplan_serie_overview"][
                                          "T.beløp"].values())[::-1]

                principal_values_period = [
                    int(val.replace("kr", "").replace(" ", "").replace("\xa0", ""))
                    for val in principal_period]
                payment_values_serie_period = [
                    int(val.replace("kr", "").replace(" ", "").replace("\xa0", ""))
                    for val in payment_period]

                self.bar_plot_serie_period = StackedBarChartWithLine(
                    termin, payment_values_serie_period, principal_values_period,
                    self.parent.parent.ui_form.graphics_view_serie_period,
                    self.parent.parent.ui_form.table_view_serie_overview,
                    y_max=int(max(payment_values_annuitet_period) * 1.33))

                self.bar_plot_serie_period.table_view_mapping()

            self.configure_charts()

            self.data.update(restructure_data)
            self.parent.close()

    def configure_charts(self):
        """
        method for configuring charts

        """
        self.parent.parent.ui_form.table_view_annuitet_overview.horizontalHeader() \
            .setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.parent.parent.ui_form.table_view_annuitet_overview.horizontalHeader() \
            .setSectionResizeMode(1, QHeaderView.Stretch)
        self.parent.parent.ui_form.table_view_annuitet_overview.horizontalHeader() \
            .setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.parent.parent.ui_form.table_view_annuitet_overview.horizontalHeader() \
            .setSectionResizeMode(3, QHeaderView.Stretch)
        self.parent.parent.ui_form.table_view_annuitet_overview.horizontalHeader() \
            .setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.parent.parent.ui_form.table_view_annuitet_overview.horizontalHeader() \
            .setSectionResizeMode(5, QHeaderView.Stretch)
        self.parent.parent.ui_form.table_view_annuitet_overview.horizontalHeader() \
            .setSectionResizeMode(6, QHeaderView.ResizeToContents)

        self.parent.parent.ui_form.table_view_serie_overview.horizontalHeader() \
            .setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.parent.parent.ui_form.table_view_serie_overview.horizontalHeader() \
            .setSectionResizeMode(1, QHeaderView.Stretch)
        self.parent.parent.ui_form.table_view_serie_overview.horizontalHeader() \
            .setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.parent.parent.ui_form.table_view_serie_overview.horizontalHeader() \
            .setSectionResizeMode(3, QHeaderView.Stretch)
        self.parent.parent.ui_form.table_view_serie_overview.horizontalHeader() \
            .setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.parent.parent.ui_form.table_view_serie_overview.horizontalHeader() \
            .setSectionResizeMode(5, QHeaderView.Stretch)
        self.parent.parent.ui_form.table_view_serie_overview.horizontalHeader() \
            .setSectionResizeMode(6, QHeaderView.ResizeToContents)

        for graphics_view in ['graphics_view_annuitet_overview', 'graphics_view_serie_overview',
                              'graphics_view_annuitet_period', 'graphics_view_serie_period']:
            getattr(self.parent.parent.ui_form, graphics_view).setMouseEnabled(x=False, y=False)
            getattr(self.parent.parent.ui_form, graphics_view).getAxis('left').setStyle(
                showValues=False)
            getattr(self.parent.parent.ui_form, graphics_view).getAxis('bottom').setStyle(
                showValues=False)
            getattr(self.parent.parent.ui_form, graphics_view).hideButtons()
            getattr(self.parent.parent.ui_form, graphics_view).setMenuEnabled(False)
            getattr(self.parent.parent.ui_form, graphics_view).showGrid(x=True, y=True)

    def clear_all(self):
        """
        method for clearing all line_edits and combo_boxes in model

        """
        StackedBarChartWithLine.clear_graphics(
            self.parent.parent.ui_form.graphics_view_annuitet_overview,
            self.parent.parent.ui_form.table_view_annuitet_overview)
        StackedBarChartWithLine.clear_graphics(
            self.parent.parent.ui_form.graphics_view_serie_overview,
            self.parent.parent.ui_form.table_view_serie_overview)

        StackedBarChartWithLine.clear_graphics(
            self.parent.parent.ui_form.graphics_view_annuitet_period,
            self.parent.parent.ui_form.table_view_annuitet_overview)
        StackedBarChartWithLine.clear_graphics(
            self.parent.parent.ui_form.graphics_view_serie_period,
            self.parent.parent.ui_form.table_view_serie_overview)

        self.clear_combo_boxes(["lanetype", "intervall", "laneperiode"])
        self.clear_date_edits(["startdato"])
        self.clear_line_edits(["egenkapital", "belaning", "nominell_rente"])
        self.data = {}
