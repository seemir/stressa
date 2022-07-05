# -*- coding: utf-8 -*-
"""
Module containing logic for table with Payment plan

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pandas as pd

from PyQt5.QtCore import QObject, pyqtSlot
from source.util import Assertor

from .table_model import TableModel
from .model import Model


class PaymentModel(Model):
    """
    Implementation of model for Payment plan

    """

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

        if "nedbetalingsplan_annuitet" in analysis_model.data.keys():
            payment_data_model_fixed = TableModel(
                pd.DataFrame(analysis_model.data["nedbetalingsplan_annuitet"]))
            self.parent.ui_form.table_view_annuitet.setModel(payment_data_model_fixed)
        if "nedbetalingsplan_serie" in analysis_model.data.keys():
            payment_data_model_serie = TableModel(
                pd.DataFrame(analysis_model.data["nedbetalingsplan_serie"]))
            self.parent.ui_form.table_view_serie.setModel(payment_data_model_serie)

    def clear_all(self):
        """
        method for clearing data in model

        """
        self.parent.ui_form.table_view_annuitet.setModel(None)
        self.parent.ui_form.table_view_annuitet.clearSpans()
