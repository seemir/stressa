# -*- coding: utf-8 -*-
"""
Module for restructure view

"""
__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

from PyQt5.uic import loadUi  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QDialog, \
    QWidget  # pylint: disable=no-name-in-module
from PyQt5.QtCore import pyqtSlot, Qt, \
    QDate  # pylint: disable=no-name-in-module

from source.util import Assertor
from source.domain import Money

from ..models import RestructureModel

from .meta_view import MetaView


class RestructureView(QDialog):
    """
    Restructure dialog window

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
        self.ui_form = loadUi(os.path.join(os.path.dirname(__file__),
                                           "forms/restructure_form.ui"), self)
        self.ui_form.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui_form.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        self._error_view = self.parent.error_view
        self._meta_view = MetaView(self)

        self._restructure_model = RestructureModel(self)
        self.restructure_model.restructure_info()

        self.ui_form.push_button_budget_meta_data.clicked.connect(
            self.meta_view.display)
        self.ui_form.push_button_avbryt.clicked.connect(self.close)
        self.ui_form.push_button_tom_skjema.clicked.connect(
            self.restructure_model.clear_all)
        self.ui_form.push_button_eksporter.clicked.connect(
            self.restructure_model.export)

    @property
    def parent(self):
        """
        parent getter

        Returns
        -------
        out     : QObject
                  active parent view

        """
        return self._parent

    @property
    def restructure_model(self):
        """
        restructure model getter

        Returns
        -------
        out     : QObject
                  active parent view

        """
        return self._restructure_model

    @property
    def error_view(self):
        """
        ErrorView getter

        Returns
        -------
        out     : QObject
                  active ErrorView

        """
        return self._error_view

    @property
    def meta_view(self):
        """
        MetaView getter

        Returns
        -------
        out     : MetaView
                  View with the metadata

        """
        return self._meta_view

    @pyqtSlot()
    def display(self):
        """
        method for showing form

        """
        # mortgage structure information
        mortgage_model = self.parent.mortgage_model.data
        analysis_model = self.parent.analysis_model.data

        if "lanetype" in mortgage_model and "lanetype" not in \
                self.restructure_model.data:
            self.ui_form.combo_box_lanetype.setCurrentText(
                mortgage_model["lanetype"])
            self.restructure_model.set_combo_box("lanetype")
        if "intervall" in mortgage_model and "intervall" not in \
                self.restructure_model.data:
            self.ui_form.combo_box_intervall.setCurrentText(
                mortgage_model["intervall"])
            self.restructure_model.set_combo_box("intervall")
        if "laneperiode" in mortgage_model and "laneperiode" not in \
                self.restructure_model.data:
            self.ui_form.combo_box_laneperiode.setCurrentText(
                mortgage_model["laneperiode"])
            self.restructure_model.set_combo_box("laneperiode")
        if "startdato" in mortgage_model and "startdato" not in \
                self.restructure_model.data:
            startdate = QDate.fromString(mortgage_model["startdato"],
                                         "dd.MM.yyyy")
            self.ui_form.date_edit_startdato.setDate(startdate)
            self.restructure_model.set_date_edit("startdato")
        if "egenkapital" in mortgage_model and "egenkapital" not in \
                self.restructure_model.data:
            self.ui_form.line_edit_egenkapital.setText(
                mortgage_model["egenkapital"])
            self.restructure_model.set_line_edit("egenkapital", Money, "value")
        if "belaning" in analysis_model and "belaning" not in \
                self.restructure_model.data:
            self.ui_form.line_edit_belaning.setText(analysis_model["belaning"])
            self.restructure_model.set_line_edit("belaning", Money, "value")

        self.ui_form.combo_box_lanetype.setFocus()
        self.show()
