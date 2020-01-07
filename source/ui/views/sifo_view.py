# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

"""
SifoView which contains the GUI for the SIFO calculator

"""

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
        super(SifoView, self).__init__(parent=parent)
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "forms/sifo_form.ui"), self)
        self.ui.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.ui.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self._parent = parent
        self._sifo_model = SifoModel(self)
        self._error = self.parent.error
        self._meta_view = MetaView(self)
        self.ui.push_button_metadata.clicked.connect(self._meta_view.show)

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
    def error(self):
        """
        ErrorView getter

        Returns
        -------
        out     : QObject
                  active ErrorView in the SifoView

        """
        return self._error
