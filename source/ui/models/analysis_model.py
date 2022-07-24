# -*- coding: utf-8 -*-
"""
Model with Analysis logic of mortgages

"""
__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pandas as pd

from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtCore import QObject, Qt

from source.app import MortgageAnalysisProcess
from source.domain import Mortgage
from source.util import Assertor

from .table_model import TableModel
from .model import Model


class AnalysisModel(Model):
    """
    Implementation of the Analysis model for which mortgages are analysed

    """

    _analysis_keys = ['arsinntekt_aar', 'belaning', 'belaningsgrad', 'egenkapital_2',
                      'egenkapital_andel', 'netto_likviditet_2', 'total_ramme', 'krav_belaning',
                      'krav_egenkapital_andel', 'krav_belaningsgrad', 'krav_total_ramme',
                      'krav_egenkapital', 'stresstest_annuitet', 'stresstest_serie',
                      'krav_stresstest_annuitet', 'krav_stresstest_serie', 'krav_nettolikviditet']

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

        self.parent.ui_form.push_button_analyse.clicked.connect(self.analyze_mortgage)

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

        if all(element in self.data.keys() for element in Mortgage.requirements_mortgage):
            self.parent.restructure_model.clear_all()
            self.parent.payment_model.clear_all()

            self.parent.ui_form.tab_widget_home.setCurrentIndex(1)

            mortgage_analysis_data = MortgageAnalysisProcess(self.data).mortgage()
            self.set_line_edits(line_edit_text='', line_edits=self.analysis_keys,
                                data=mortgage_analysis_data)

            if "nedbetalingsplan_annuitet_overview" in mortgage_analysis_data.keys():
                payment_data_model_fixed = TableModel(
                    pd.DataFrame(mortgage_analysis_data["nedbetalingsplan_annuitet_overview"]),
                    alignment=Qt.AlignCenter)
                self.parent.ui_form.table_view_annuitet_overview.setModel(payment_data_model_fixed)
            if "nedbetalingsplan_serie_overview" in mortgage_analysis_data.keys():
                payment_data_model_serie = TableModel(
                    pd.DataFrame(mortgage_analysis_data["nedbetalingsplan_serie_overview"]),
                    alignment=Qt.AlignCenter)
                self.parent.ui_form.table_view_serie_overview.setModel(payment_data_model_serie)

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

            payment_keys = ["start_dato_annuitet", "slutt_dato_annuitet", "total_termin_annuitet",
                            "aar_annuitet", "termin_aar_annuitet", "laan_annuitet",
                            "rente_annuitet", "total_rente_annuitet", "total_belop_annuitet",
                            "start_dato_serie", "nedbetalingsplan_annuitet", "slutt_dato_serie",
                            "total_termin_serie", "aar_serie", "termin_aar_serie", "laan_serie",
                            "rente_serie", "total_rente_serie", "total_belop_serie",
                            "nedbetalingsplan_serie", "netto_likviditet_plan_serie",
                            "netto_likviditet_mnd_serie", "netto_likviditet_plan_annuitet",
                            "netto_likviditet_mnd_annuitet"]

            for payment_key in payment_keys:
                if payment_key in mortgage_analysis_data.keys():
                    self.data.update({payment_key: mortgage_analysis_data[payment_key]})

    def clear_all(self):
        """
        method for clearing model

        """
        self.data = {}
        self.clear_line_edits(self.analysis_keys)
