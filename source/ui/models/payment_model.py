# -*- coding: utf-8 -*-
"""
Module containing logic for table with Payment plan

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pandas as pd

from PyQt5.QtCore import QObject, pyqtSlot, Qt
from source.util import Assertor

from .table_model import TableModel
from .model import Model


class PaymentModel(Model):
    """
    Implementation of model for Payment plan

    """
    payment_keys = ["start_dato_annuitet", "slutt_dato_annuitet", "total_termin_annuitet",
                    "aar_annuitet", "termin_aar_annuitet", "laan_annuitet", "rente_annuitet",
                    "total_rente_annuitet", "total_belop_annuitet", "start_dato_serie",
                    "slutt_dato_serie", "total_termin_serie", "aar_serie",
                    "termin_aar_serie", "laan_serie", "rente_serie",
                    "total_rente_serie", "total_belop_serie", "netto_likviditet_plan_serie",
                    "netto_likviditet_mnd_serie", "netto_likviditet_plan_annuitet",
                    "netto_likviditet_mnd_annuitet"]

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

    @pyqtSlot()
    def generate_payment_plan(self):
        """
        method for payment plan to front end

        """
        analysis_model = self.parent.parent.analysis_model
        restructure_model = self.parent.parent.restructure_model

        if all(val in restructure_model.data.keys() for val in self.payment_keys):
            if "nedbetalingsplan_annuitet" in restructure_model.data.keys():
                payment_data_model_fixed = TableModel(
                    pd.DataFrame(restructure_model.data["nedbetalingsplan_annuitet"]),
                    alignment=Qt.AlignCenter)
                self.parent.ui_form.table_view_annuitet.setModel(payment_data_model_fixed)
            if "nedbetalingsplan_serie" in restructure_model.data.keys():
                payment_data_model_serie = TableModel(
                    pd.DataFrame(restructure_model.data["nedbetalingsplan_serie"]),
                    alignment=Qt.AlignCenter)
                self.parent.ui_form.table_view_serie.setModel(payment_data_model_serie)

            self.set_line_edits("", line_edits=self.payment_keys, data=restructure_model.data)

        elif all(val in analysis_model.data.keys() for val in self.payment_keys):
            if "nedbetalingsplan_annuitet" in analysis_model.data.keys():
                payment_data_model_fixed = TableModel(
                    pd.DataFrame(analysis_model.data["nedbetalingsplan_annuitet"]),
                    alignment=Qt.AlignCenter)
                self.parent.ui_form.table_view_annuitet.setModel(payment_data_model_fixed)
            if "nedbetalingsplan_serie" in analysis_model.data.keys():
                payment_data_model_serie = TableModel(
                    pd.DataFrame(analysis_model.data["nedbetalingsplan_serie"]),
                    alignment=Qt.AlignCenter)
                self.parent.ui_form.table_view_serie.setModel(payment_data_model_serie)

            self.set_line_edits("", line_edits=self.payment_keys, data=analysis_model.data)

    def clear_all(self):
        """
        method for clearing data in model

        """
        self.parent.ui_form.table_view_annuitet.setModel(None)
        self.parent.ui_form.table_view_annuitet.clearSpans()
        self.parent.ui_form.table_view_serie.setModel(None)
        self.parent.ui_form.table_view_serie.clearSpans()
        self.clear_line_edits(self.payment_keys)
