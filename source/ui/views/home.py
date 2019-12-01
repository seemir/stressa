# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot
from PyQt5.uic import loadUi

from .sifo_calc import SifoCalc
from .error import Error
from . import resources

from ..models import Formatting


class HomePage(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "forms/home.ui"), self)
        self._formatting = Formatting(self, Error)

        self._formatting.format_contact_info()

    @pyqtSlot()
    def open_sifo_calculator(self):
        calculator = SifoCalc(self)
        calculator.exec_()
