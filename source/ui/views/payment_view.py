# -*- coding: utf-8 -*-
"""
Module with logic for the View that handles the Payment plan

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

from PyQt5.uic import loadUi  # pylint: disable=no-name-in-module
from PyQt5.QtCore import Qt  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QDialog, QWidget, \
    QHeaderView  # pylint: disable=no-name-in-module

from source.util import Assertor

from ..models import PaymentModel


class PaymentView(QDialog):
    """
    Implementation of model for Payment plan view

    """

    def __init__(self, parent: QWidget):
        """
        Constructor / Instantiation of class

        Parameters
        ----------
        parent  : QWidget
                  parent view of the PaymentView

        """
        super().__init__(parent)
        Assertor.assert_data_types([parent], [QWidget])
        self.parent = parent
        self.ui_form = loadUi(
            os.path.join(os.path.dirname(__file__), "forms/payment_form.ui"),
            self)
        self.ui_form.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui_form.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.ui_form.table_view_annuitet.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.ui_form.table_view_serie.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)

        self.payment_model = PaymentModel(self)

    def display(self):
        """
        method for displaying payment plan

        """
        self.payment_model.generate_payment_plan()
        self.show()
