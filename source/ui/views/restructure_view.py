# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.uic import loadUi

from source.util import Assertor

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
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "forms/restructure_form.ui"), self)
        self.ui.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        self._error_view = self.parent.error_view
        self._meta_view = MetaView(self)

        self.ui.push_button_budget_meta_data.clicked.connect(self.meta_view.display)
        self.ui.push_button_avbryt.clicked.connect(self.close)

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
        self.ui.combo_box_lanetype.setFocus()
        self.show()
