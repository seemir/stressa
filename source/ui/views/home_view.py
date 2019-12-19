# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from source.ui.models import ContactModel, BudgetModel, FinnModel, MortgageModel

from .sifo_view import SifoView
from .error_view import ErrorView
from . import resources


class HomeView(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "forms/home_form.ui"), self)

        self._error = ErrorView(self)
        self._contact_model = ContactModel(self)
        self._budget_model = BudgetModel(self)
        self._finn_model = FinnModel(self)
        self._mortgage_model = MortgageModel(self)

        self._sifo_view = SifoView(self)

        self._contact_model.contact_info()
        self._budget_model.budget_info()
        self._finn_model.finn_info()
        self._mortgage_model.mortgage_info()

        self.ui.push_button_sifo_utgifter.clicked.connect(self.show_sifo_calculator)

    @property
    def error(self):
        return self._error

    def show_sifo_calculator(self):
        self._sifo_view.sifo_model.show_sifo_calculator()
