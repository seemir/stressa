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
from PyQt5.uic import loadUi

from source.ui.models import MortgageModel, FinnModel, HomeModel

from .error_view import ErrorView
from .sifo_view import SifoView
from .meta_view import MetaView

from . import resources


# myappid = 'mycompany.myproduct.subproduct.version'
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

        self._error = ErrorView(self)
        self._sifo_view = SifoView(self)
        self._meta_view = MetaView(self)

        self._sifo_model = self.sifo_view.sifo_model
        self._mortgage_model = MortgageModel(self)
        self._finn_model = FinnModel(self)

        self._mortgage_model.mortgage_info()
        self._finn_model.finn_info()

        self.ui.push_button_sifo_utgifter.clicked.connect(self.sifo_view.display)

        self.ui.push_button_finn_1.clicked.connect(
            lambda: self.finn_model.open_finn_url("finnkode_1"))
        self.ui.push_button_hent_finn_data_1.clicked.connect(
            lambda: self.finn_model.add_finn_info("_1"))

        self.ui.push_button_home_meta_data.clicked.connect(self._meta_view.show)

        self._home_model = HomeModel(self)
        self.ui.push_button_tom_skjema.clicked.connect(self.home_model.clear_all)

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
    def error(self):
        """
        ErrorView getter

        Returns
        -------
        out     : QObject
                  active ErrorView in class

        """
        return self._error

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
