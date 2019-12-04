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

from ..models import ContactModel, BudgetModel, FinnModel, MortgageModel


class HomePage(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "forms/home.ui"), self)

        self._contact_model = ContactModel(self, Error)
        self._budget_model = BudgetModel(self, Error)
        self._finn_model = FinnModel(self, Error)
        self._mortgage_model = MortgageModel(self, Error)

        self._contact_model.contact_info()
        self._budget_model.budget_info()
        self._finn_model.finn_info()
        self._mortgage_model.mortgage_information()

    @pyqtSlot()
    def open_sifo_calculator(self):
        calculator = SifoCalc(self)
        calculator.exec_()
