# -*- coding: utf-8 -*-

"""
The main HomeView of the Application, i.e. the first view that the viewer is meet with after
the splash screen

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
# import ctypes

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot
from PyQt5.uic import loadUi

from ..models import MortgageModel, FinnModel, HomeModel

from .statistics_view import StatisticsView
from .grunnboka_view import GrunnbokaView
from .history_view import HistoryView
from .budget_view import BudgetView
from .error_view import ErrorView
from .sifo_view import SifoView
from .meta_view import MetaView
from .tax_view import TaxView

from . import resources


# myappid = 'Stressa.stressa.ui.version'
# ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class HomeView(QMainWindow):
    """
    The HomeView which is the only QMainWindow in the application

    """

    def __init__(self):
        """
        Constructor / instantiating the class

        """
        super().__init__()
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "forms/home_form.ui"), self)

        self._error_view = ErrorView(self)
        self._budget_view = BudgetView(self)
        self._tax_view = TaxView(self)
        self._sifo_view = SifoView(self)
        self._history_view = HistoryView(self)
        self._grunnboka_view = GrunnbokaView(self)

        self._meta_view = MetaView(self)
        self._statistics_view = StatisticsView(self)
        self._home_model = HomeModel(self)

        self._sifo_model = self.sifo_view.sifo_model
        self._mortgage_model = MortgageModel(self)
        self._finn_model = FinnModel(self)
        self._budget_model = self.budget_view.budget_model
        self._tax_model = self.tax_view.tax_model

        self._mortgage_model.mortgage_info()
        self._finn_model.finn_info()
        self._budget_view.budget_info()
        self._home_model.liquidity_info()

        self.ui.push_button_budsjett.clicked.connect(self.budget_view.display)
        self.ui.push_button_skatt.clicked.connect(self.tax_view.display)
        self.ui.push_button_sifo_utgifter.clicked.connect(self.sifo_view.display)

        self.ui.push_button_home_meta_data.clicked.connect(self._meta_view.display)
        self.ui.push_button_tom_skjema.clicked.connect(self.home_model.clear_all)
        self.ui.action_logo.triggered.connect(self.info_tab)

    @property
    def error_view(self):
        """
        ErrorView getter

        Returns
        -------
        out     : QObject
                  active ErrorView in class

        """
        return self._error_view

    @property
    def budget_view(self):
        """
        BudgetView getter

        Returns
        -------
        out     : QObject
                  active BudgetView in class

        """
        return self._budget_view

    @property
    def tax_view(self):
        """
        TaxView getter

        Returns
        -------
        out     : TaxView
                  Active TaxView in the HomeView

        """
        return self._tax_view

    @property
    def sifo_view(self):
        """
        SifoView getter

        Returns
        -------
        out     : SifoView
                  Active SifoView in the HomeView

        """
        return self._sifo_view

    @property
    def meta_view(self):
        """
        MetaView getter

        Returns
        -------
        out     : QObject
                  active MetaView class

        """
        return self._meta_view

    @property
    def history_view(self):
        """
        HistoryView getter

        Returns
        -------
        out     : QObject
                  active HistoryView class

        """
        return self._history_view

    @property
    def grunnboka_view(self):
        """
        GrunnbokaView getter

        Returns
        -------
        out     : GrunnbokaView
                  View with the link to the Grunnboka

        """
        return self._grunnboka_view

    @property
    def statistics_view(self):
        """
        StatisticsView getter

        Returns
        -------
        out     : QObject
                  active StatisticsView class

        """
        return self._statistics_view

    @property
    def mortgage_model(self):
        """
        MortgageModel getter

        Returns
        -------
        out     : MortgageModel
                  active MortgageModel in HomeView

        """
        return self._mortgage_model

    @property
    def finn_model(self):
        """
        FinnModel getter

        Returns
        -------
        out     : FinnModel
                  Active FinnModel in HomeView

        """
        return self._finn_model

    @property
    def home_model(self):
        """
        HomeModel getter

        Returns
        -------
        out     : HomeModel
                  Active HomeModel in Homeview

        """
        return self._home_model

    @property
    def sifo_model(self):
        """
        SifoModel getter

        Returns
        -------
        out     : SifoModel
                  Active SifoModel in the SifoView

        """
        return self._sifo_model

    @property
    def budget_model(self):
        """
        BudgetModel getter

        Returns
        -------
        out     : BudgetModel
                  Active BudgetModel in the BudgetView

        """
        return self._budget_model

    @property
    def tax_model(self):
        """
        TaxModel getter

        Returns
        -------
        out     : TaxModel
                  Active TaxModel in the BudgetView

        """
        return self._tax_model

    @pyqtSlot()
    def info_tab(self):
        """
        method for returning to info tab in HomeView

        """
        self.ui.tab_widget_home.setCurrentIndex(0)
