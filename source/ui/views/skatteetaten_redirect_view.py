# -*- coding: utf-8 -*-

"""
A dialog window for redirecting user to correct Skatteetaten form

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

from typing import Union

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QObject

from source.util import Assertor

from .skatteetaten_calculator_view import SkatteetatenCalculatorView
from .skatteetaten_import_view import SkatteetatenImportView


class SkatteetatenRedirectView(QDialog):
    """
    Tax redirect model

    """

    def __init__(self, parent: Union[QObject, None]):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        parent      : QObject
                      parent class for which this dialog window is part

        """
        Assertor.assert_data_types([parent], [(QObject, type(None))])
        super().__init__(None)

        self.parent = parent

        self._skatteetaten_calculator_view = SkatteetatenCalculatorView(self)
        self._skatteetaten_import_view = SkatteetatenImportView(self)

        self.ui_form = loadUi(
            os.path.join(os.path.dirname(__file__), "forms/skatteetaten_redirect_form.ui"),
            self)
        self.ui_form.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui_form.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        self.ui_form.push_button_cancel.clicked.connect(self.close)

        self.ui_form.push_button_skattekalkulator.clicked.connect(
            self.skatteetaten_calculator_display)
        self.ui_form.push_button_hent_skatteetaten.clicked.connect(
            self.skatteetaten_import_display)

    @property
    def skatteetaten_calculator_view(self):
        """
        getter for Skatteetaten calculator view

        Returns
        -------
        out             : SkatteetatenCalculatorView
                          active SkatteCalculatorView in class

        """
        return self._skatteetaten_calculator_view

    @property
    def skatteetaten_import_view(self):
        """
        getter for Skatteetaten import view

        Returns
        -------
        out             : SkatteetatenImportView
                          active SkatteImportView in class

        """
        return self._skatteetaten_import_view

    def skatteetaten_calculator_display(self):
        """
        method for displaying Skatteetaten calculator

        """
        self.skatteetaten_calculator_view.display()
        self.close()

    def skatteetaten_import_display(self):
        """
        method for displaying Skatteetaten import view

        """
        self.skatteetaten_import_view.display()
        self.close()
