# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import pyqtSlot
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

from source.util import Assertor

from .meta_view import MetaView
from ..models import TaxModel


class TaxView(QDialog):
    """
    Tax dialog window

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
        self._parent = parent
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "forms/tax_form.ui"), self)
        self.ui.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        self._error_view = self.parent.error_view
        self._meta_view = MetaView(self)

        self._tax_model = TaxModel(self)

        self.ui.push_button_utregning.clicked.connect(self.calculate_tax_income)
        self.ui.push_button_tom_skjema.clicked.connect(self.clear_all)
        self.ui.push_button_meta_data_1.clicked.connect(self.meta_view.display)
        self.ui.push_button_avbryt_1.clicked.connect(self.close)

        self.ui.push_button_tilbake.clicked.connect(self.back)
        self.ui.push_button_meta_data_2.clicked.connect(self.meta_view.display)
        self.ui.push_button_avbryt_2.clicked.connect(self.close)

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
    def tax_model(self):
        return self._tax_model

    @pyqtSlot()
    def display(self):
        self.tax_model.tax_info()
        self.show()

    def back(self):
        """
        method for returning for results page to input page

        """
        self.ui.tab_widget_skattekalkulator.setCurrentIndex(0)

    @pyqtSlot()
    def calculate_tax_income(self):
        self.tax_model.calculate_tax_income()

    @pyqtSlot()
    def clear_all(self):
        self.ui.combo_box_tax_year.setCurrentIndex(0)
        self.tax_model.clear_combo_boxes(["skatte_aar"])
        self.tax_model.clear_line_edit("alder")
        self.tax_model.clear_line_edit("fagforeningskontigent")
        self.tax_model.clear_line_edits(self.tax_model.total_posts)

        self.tax_model.clear_line_edit("bsu")
        self.tax_model.clear_line_edit("verdi_primarbolig")
        self.tax_model.clear_line_edit("bankinnskudd")
        self.tax_model.clear_line_edit("gjeld")
        self.tax_model.clear_line_edit("netto_formue")

        self.tax_model.clear_line_edits(self.tax_model.tax_output)
        self.ui.combo_box_tax_year.setFocus()
