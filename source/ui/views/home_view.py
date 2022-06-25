# -*- coding: utf-8 -*-

"""
The main HomeView of the Application, i.e. the first view that the viewer is meet with after
the splash screen

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
import shutil
# import ctypes
import sys

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi

from ..models import MortgageModel, FinnModel, HomeModel, AnalysisModel

from .restructure_view import RestructureView
from .statistics_view import StatisticsView
from .info_view_clear import InfoViewClear
from .grunnboka_view import GrunnbokaView
from .info_view_quit import InfoViewQuit
from .history_view import HistoryView
from .budget_view import BudgetView
from .error_view import ErrorView
from .sifo_view import SifoView
from .meta_view import MetaView

from .tax_view import TaxView


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
        dir_up = os.path.dirname
        self.ui_form = loadUi(os.path.join(dir_up(__file__), "forms/home_form.ui"), self)

        self._error_view = ErrorView(self)
        self._budget_view = BudgetView(self)
        self._tax_view = TaxView(self)
        self._sifo_view = SifoView(self)
        self._history_view = HistoryView(self)
        self._grunnboka_view = GrunnbokaView(self)

        self._meta_view = MetaView(self)
        self._info_view_quit = InfoViewQuit(self)
        self._info_view_clear = InfoViewClear(self)
        self._statistics_view = StatisticsView(self)

        self._home_model = HomeModel(self)
        self._finn_model = FinnModel(self)
        self._mortgage_model = MortgageModel(self)

        self._tax_model = self.tax_view.tax_model
        self._sifo_model = self.sifo_view.sifo_model
        self._budget_model = self.budget_view.budget_model

        self._analysis_model = AnalysisModel(self)
        self._restructure_view = RestructureView(self)
        self._restructure_model = self.restructure_view.restructure_model

        self._mortgage_model.mortgage_info()
        self._finn_model.finn_info()
        self._budget_view.budget_info()
        self._home_model.liquidity_info()

        self.ui_form.push_button_budsjett.clicked.connect(self.budget_view.display)
        self.ui_form.push_button_skatt.clicked.connect(self.tax_view.display)
        self.ui_form.push_button_sifo_utgifter.clicked.connect(self.sifo_view.display)

        self.ui_form.push_button_home_meta_data.clicked.connect(self._meta_view.display)
        self.ui_form.push_button_tom_skjema.clicked.connect(self.clear_all)
        self.ui_form.push_button_avslutt.clicked.connect(self.avslutt)
        self.ui_form.action_logo.triggered.connect(self.info_tab)

        self.ui_form.push_button_restructure.clicked.connect(self.restructure_view.display)

        self.ui_form.push_button_restructure.setIcon(
            QIcon(dir_up(dir_up(os.path.abspath(__file__))) + '/images/restructure.png'))

    def closeEvent(self, event):
        """
        handler of closeEvents

        """
        self.avslutt()
        event.ignore()

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
    def restructure_model(self):
        """
        Restructure model getter

        Returns
        -------
        out     : QObject
                  active Restructure model in class

        """
        return self._restructure_model

    @property
    def restructure_view(self):
        """
        Restructure getter

        Returns
        -------
        out     : QObject
                  active Restructure in class

        """
        return self._restructure_view

    @property
    def info_view_quit(self):
        """
        InfoView getter

        Returns
        -------
        out     : QObject
                  active InfoView in class

        """
        return self._info_view_quit

    @property
    def info_view_clear(self):
        """
        InfoView getter

        Returns
        -------
        out     : QObject
                  active InfoView in class

        """
        return self._info_view_clear

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
    def analysis_model(self):
        """
        AnalysisModel getter

        Returns
        -------
        out     : AnalysisModel
                  active AnalysisModel in HomeView

        """
        return self._analysis_model

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
        self.ui_form.tab_widget_home.setCurrentIndex(0)

    @pyqtSlot()
    def clear_all(self):
        """
        method for clearing all data

        """
        self.info_view_clear.show()
        self.info_view_clear.push_button_apply.clicked.connect(self.apply_clearing)
        self.info_view_clear.push_button_cancel.clicked.connect(self.info_view_clear.close)

    @pyqtSlot()
    def apply_clearing(self):
        """
        method for applying clearing

        """
        self.home_model.clear_all()
        self.info_view_clear.close()

    @pyqtSlot()
    def avslutt(self):
        """
        method for quiting app

        """
        self.info_view_quit.show()
        self.info_view_quit.push_button_cancel.clicked.connect(self.info_view_quit.close)
        self.info_view_quit.push_button_apply.clicked.connect(self.avslutt_alt)

    @pyqtSlot()
    def avslutt_alt(self):
        """
        method for quiting and deleting all data

        """
        self.delete_temp_folder()
        self.info_view_quit.close()
        sys.exit()

    def delete_temp_folder(self):
        """
        method for deleting temp folder

        """
        dir_path = self.grunnboka_view.download_path
        for filename in os.listdir(dir_path):
            filepath = os.path.join(dir_path, filename)
            try:
                shutil.rmtree(filepath)
            except OSError:
                os.remove(filepath)
