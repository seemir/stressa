# -*- coding: utf-8 -*-
"""
SifoView which contains the GUI for the SIFO calculator

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi

from source.ui.models import SifoModel
from source.util import Assertor

from .meta_view import MetaView

from . import resources


class SifoView(QDialog):
    """
    Sifo Calculator view

    """

    def __init__(self, parent: QWidget):
        """
        Constructor / Instantiation of class

        Parameters
        ----------
        parent  : QWidget
                  parent view for the SifoView

        """
        Assertor.assert_data_types([parent], [QWidget])
        super().__init__(parent=parent)
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "forms/sifo_form.ui"), self)
        self.ui.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.ui.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self._parent = parent
        self._sifo_model = SifoModel(self)
        self._error_view = self.parent.error_view
        self._meta_view = MetaView(self)

        self.ui.push_button_sifo_meta_data.clicked.connect(self.meta_view.display)
        self.ui.push_button_vis_resultatet.clicked.connect(self.sifo_model.calculate_sifo_expenses)
        self.ui.push_button_tom_skjema_1.clicked.connect(self.clear_all)
        self.ui.push_button_avbryt_1.clicked.connect(self.close)
        self.ui.push_button_tom_skjema_2.clicked.connect(self.clear_all)
        self.ui.push_button_avbryt_2.clicked.connect(self.close)
        self.ui.push_button_tilbake.clicked.connect(self.back)
        self.ui.push_button_eksporter.clicked.connect(self.export)

    @property
    def sifo_model(self):
        """
        SifoModel getter

        Returns
        -------
        out     : SifoModel
                  Model containing all the logic of the Sifo calculations

        """
        return self._sifo_model

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

    def display(self):
        """
        Method for displaying SifoView

        """
        self.sifo_model.sifo_info()
        self.show()

    def export(self):
        """
        method for exporting SIFO expenses to HomeView

        """
        sifo_expenses = self.ui.line_edit_totalt_1.text()
        if sifo_expenses:
            self.parent.mortgage_model.set_line_edit("sifo_utgifter", data=sifo_expenses)
        else:
            self.parent.mortgage_model.clear_line_edit("sifo_utgifter")
        self.close()

    def back(self):
        """
        method for returning for results page to input page

        """
        self.ui.tab_widget_sifo.setCurrentIndex(0)

    def clear_all(self):
        self.parent.mortgage_model.clear_line_edit("sifo_utgifter")
        self.sifo_model.clear_all()
