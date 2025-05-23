# -*- coding: utf-8 -*-

"""
The main HomeView of the Application, i.e. the first view that the viewer is meet with after
the splash screen

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
import ctypes
import sys

from PyQt5.uic import loadUi  # pylint: disable=no-name-in-module
from PyQt5.QtGui import QIcon  # pylint: disable=no-name-in-module
from PyQt5.QtCore import pyqtSlot  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QMainWindow  # pylint: disable=no-name-in-module

from source.util import __version__

from ..models import MortgageModel, FinnModel, HomeModel, AnalysisModel

from .restructure_view import RestructureView
from .statistics_view import StatisticsView
from .ad_history_view import AdHistoryView
from .info_clear_view import InfoClearView
from .info_quit_view import InfoQuitView
from .settings_view import SettingsView
from .payment_view import PaymentView
from .history_view import HistoryView
from .budget_view import BudgetView
from .error_view import ErrorView
from .sifo_view import SifoView
from .meta_view import MetaView

from .skatteetaten_calculator_view import SkatteetatenCalculatorView

MY_APP_ID = 'Stressa.stressa.ui.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(MY_APP_ID)


class HomeView(QMainWindow):  # pylint: disable=too-many-instance-attributes
    """
    The HomeView which is the only QMainWindow in the application

    """

    def __init__(self):
        """
        Constructor / instantiating the class

        """
        super().__init__()
        dir_up = os.path.dirname
        self.ui_form = loadUi(
            os.path.join(dir_up(__file__), "forms/home_form.ui"), self)

        self.setWindowTitle(f"Stressa v.{__version__}")

        self._error_view = ErrorView(self)
        self._budget_view = BudgetView(self)

        self._sifo_view = SifoView(self)
        self._history_view = HistoryView(self)
        self._ad_history_view = AdHistoryView(self)

        self._meta_view = MetaView(self)
        self._info_view_quit = InfoQuitView(self)
        self._info_view_clear = InfoClearView(self)
        self._statistics_view = StatisticsView(self)

        self._settings_view = SettingsView(self)

        self._home_model = HomeModel(self)
        self._finn_model = FinnModel(self)
        self._mortgage_model = MortgageModel(self)

        self._sifo_model = self.sifo_view.sifo_model
        self._budget_model = self.budget_view.budget_model

        self._analysis_model = AnalysisModel(self)
        self._restructure_view = RestructureView(self)
        self._restructure_model = self.restructure_view.restructure_model

        self._payment_view = PaymentView(self)
        self._payment_model = self.payment_view.payment_model

        self._mortgage_model.mortgage_info()
        self._finn_model.finn_info()
        self._budget_view.budget_info()
        self._home_model.liquidity_info()

        self._skatteetaten_calculator_view = SkatteetatenCalculatorView(self)

        self.ui_form.push_button_budsjett.clicked.connect(
            self.budget_view.display)
        self.ui_form.push_button_skatt.clicked.connect(
            self.skatteetaten_calculator_view.display)
        self.ui_form.push_button_sifo_utgifter.clicked.connect(
            self.sifo_view.display)

        self.ui_form.push_button_home_meta_data.clicked.connect(
            self._meta_view.display)
        self.ui_form.push_button_tom_skjema.clicked.connect(self.clear_all)
        self.ui_form.push_button_avslutt.clicked.connect(self.avslutt)
        self.ui_form.action_logo.triggered.connect(self.info_tab)

        self.ui_form.push_button_restructure.clicked.connect(
            self.restructure_view.display)
        self.ui_form.push_button_payment_plan.clicked.connect(
            self.payment_view.display)

        self.ui_form.push_button_instillinger.clicked.connect(
            self.settings_view.show)
        self.ui_form.action_instillinger.triggered.connect(
            self.settings_view.show)

        self.ui_form.push_button_restructure.setIcon(
            QIcon(dir_up(
                dir_up(os.path.abspath(__file__))) + '/images/restructure.png'))
        self.ui_form.push_button_payment_plan.setIcon(
            QIcon(
                dir_up(dir_up(os.path.abspath(__file__))) + '/images/plan.png'))

        self.analysis_model.config_plots()

    @property
    def payment_view(self):
        """
        Payment view getter

        Returns
        -------
        out     : QObject
                  active Payment view in class

        """
        return self._payment_view

    @property
    def payment_model(self):
        """
        Payment model getter

        Returns
        -------
        out     : QObject
                  active Payment model in class

        """
        return self._payment_model

    def closeEvent(self, event):  # pylint: disable=invalid-name
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
    def settings_view(self):
        """
        SettingsView getter

        Returns
        -------
        out     : QObject
                  active SettingsView in class

        """
        return self._settings_view

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
    def skatteetaten_calculator_view(self):
        """
        Skatteetaten calculator view redirect getter

        Returns
        -------
        out     : SkatteetatenCalculatorView
                  Active SkatteetatenRedirectView in the HomeView

        """
        return self._skatteetaten_calculator_view

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
    def ad_history_view(self):
        """
        AdHistoryView getter

        Returns
        -------
        out     : QObject
                  active AdHistoryView class

        """
        return self._ad_history_view

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
        self.info_view_clear.push_button_apply.clicked.connect(
            self.apply_clearing)
        self.info_view_clear.push_button_cancel.clicked.connect(
            self.info_view_clear.close)

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
        self.info_view_quit.push_button_cancel.clicked.connect(
            self.info_view_quit.close)
        self.info_view_quit.push_button_apply.clicked.connect(self.avslutt_alt)

    @pyqtSlot()
    def avslutt_alt(self):
        """
        method for quiting and deleting all data

        """
        self.info_view_quit.close()
        sys.exit()
