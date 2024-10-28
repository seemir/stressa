# -*- coding: utf-8 -*-
"""
Module containing front-end element for tax view

"""
__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

from PyQt5.uic import loadUi  # pylint: disable=no-name-in-module
from PyQt5.QtCore import pyqtSlot, Qt  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QDialog, \
    QWidget  # pylint: disable=no-name-in-module

from source.util import Assertor

from .meta_view import MetaView

from ..models import SkatteetatenCalculatorModel


class SkatteetatenCalculatorView(QDialog):
    """
    Tax calculator dialog window

    """

    def __init__(self, parent: QWidget):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        parent      : QObject
                      parent class for which this dialog window is part

        """
        Assertor.assert_data_types([parent], [QWidget])
        super().__init__(parent)
        dir_up = os.path.dirname
        self._parent = parent
        self.ui_form = loadUi(
            os.path.join(dir_up(__file__),
                         "forms/skatteetaten_calculator_form.ui"),
            self)
        self.ui_form.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui_form.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        self._error_view = self.parent.error_view
        self._meta_view = MetaView(self)

        self._skatteetaten_calculator_model = SkatteetatenCalculatorModel(self)

        self.ui_form.push_button_utregning.clicked.connect(
            self.calculate_tax_income)
        self.ui_form.push_button_tom_skjema.clicked.connect(self.clear_all)
        self.ui_form.push_button_meta_data_1.clicked.connect(
            self.meta_view.display)
        self.ui_form.push_button_avbryt_1.clicked.connect(self.close)

        self.ui_form.push_button_eksport.clicked.connect(self.export)
        self.ui_form.push_button_tilbake.clicked.connect(self.back)
        self.ui_form.push_button_meta_data_2.clicked.connect(
            self.meta_view.display)
        self.ui_form.push_button_avbryt_2.clicked.connect(self.close)
        self.ui_form.push_button_tom_skjema_2.clicked.connect(self.clear_all)

    @property
    def parent(self):
        """
        parent getter

        Returns
        -------
        out     : QObject
                  active parent view for the SifoView

        """
        return self._parent

    @property
    def error_view(self):
        """
        ErrorView getter

        Returns
        -------
        out     : QObject
                  active ErrorView in the SifoView

        """
        return self._error_view

    @property
    def meta_view(self):
        """
        MetaView getter

        Returns
        -------
        out     : MetaView
                  View with the metadata for the SifoView

        """
        return self._meta_view

    @property
    def skatteetaten_calculator_model(self):
        """
        tax model getter

        """
        return self._skatteetaten_calculator_model

    @pyqtSlot()
    def display(self):
        """
        method for displaying view data

        """
        self.ui_form.scroll_area_skatteetaten.verticalScrollBar().setValue(
            self.ui_form.scroll_area_skatteetaten.verticalScrollBar().minimum())
        self.ui_form.tab_widget_skattekalkulator.setCurrentIndex(0)
        self.ui_form.combo_box_skatte_aar.setFocus()
        self.skatteetaten_calculator_model.clear_line_edits(
            self.skatteetaten_calculator_model.total_posts)
        self.skatteetaten_calculator_model.tax_info()
        self.show()

    def back(self):
        """
        method for returning for results page to input page

        """
        self.ui_form.tab_widget_skattekalkulator.setCurrentIndex(0)

    @pyqtSlot()
    def calculate_tax_income(self):
        """
        method for calculating tax income

        """
        self.skatteetaten_calculator_model.calculate_tax_income()

    @pyqtSlot()
    def clear_all(self):
        """
        method for clearing all data from model

        """

        self.ui_form.scroll_area_skatteetaten.verticalScrollBar().setValue(
            self.ui_form.scroll_area_skatteetaten.verticalScrollBar().minimum())
        self.ui_form.combo_box_skatte_aar.setCurrentIndex(0)
        self.ui_form.tab_widget_skattekalkulator.setCurrentIndex(0)
        self.ui_form.combo_box_skatte_aar.setFocus()
        self.skatteetaten_calculator_model.clear_combo_boxes(["skatte_aar"])
        self.skatteetaten_calculator_model.clear_line_edit("alder")
        self.skatteetaten_calculator_model.clear_line_edit(
            "fagforeningskontigent")
        self.skatteetaten_calculator_model.clear_line_edits(
            self.skatteetaten_calculator_model.total_posts)

        self.skatteetaten_calculator_model.clear_line_edit("bsu")
        self.skatteetaten_calculator_model.clear_line_edit("verdi_primarbolig")
        self.skatteetaten_calculator_model.clear_line_edit("bankinnskudd")
        self.skatteetaten_calculator_model.clear_line_edit("gjeld")
        self.skatteetaten_calculator_model.clear_line_edit("netto_formue")

        self.skatteetaten_calculator_model.clear_line_edits(
            self.skatteetaten_calculator_model.tax_output)
        self.parent.mortgage_model.clear_line_edit(
            "beregnet_skatt_per_mnd_beloep")

        self.ui_form.combo_box_skatte_aar.setFocus()

    def export(self):
        """
        method for exporting Skatteetaten monthly tax value

        """
        monthly_tax_value = self.ui_form.line_edit_beregnet_skatt_per_mnd_beloep.text()
        if monthly_tax_value:
            self.parent.mortgage_model.set_line_edit(
                "beregnet_skatt_per_mnd_beloep",
                data=monthly_tax_value)
        else:
            self.parent.mortgage_model.clear_line_edit(
                "beregnet_skatt_per_mnd_beloep")
        self.close()
