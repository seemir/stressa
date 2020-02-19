# -*- coding: utf-8 -*-
"""
StatisticsView which contains the GUI for the Statistics from home ads

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi

from source.util import Assertor


class StatisticsView(QDialog):
    """
    Statistics view

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
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "forms/statistics_form.ui"), self)
        self.ui.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.ui.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
