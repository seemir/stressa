# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.uic import loadUi

from source.ui.models import HistoryModel
from source.util import Assertor


class HistoryView(QDialog):

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        Assertor.assert_data_types([parent], [QWidget])
        self.parent = parent
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "forms/history_form.ui"), self)
        self.ui.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self._history_model = HistoryModel(self)

    @property
    def history_model(self):
        return self._history_model

    @pyqtSlot()
    def add_finn_history(self, postfix):
        self.history_model.add_finn_history(postfix)
        self.exec_()
