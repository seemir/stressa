# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from PyQt5.QtCore import QObject

from source.app import MortgageAnalysisProcess
from source.domain import Mortgage
from source.util import Assertor

from .model import Model


class AnalysisModel(Model):
    """
    Implementation of the Analysis model for which mortgages are analysed

    """

    def __init__(self, parent: QObject):
        """
        Constructor / Instantiation of class

        Parameters
        ----------
        parent      : QObject
                      Parent view for which the model in to be linked

        """
        Assertor.assert_data_types([parent], [QObject])
        super().__init__(parent)

        self.parent.ui.push_button_analyse.clicked.connect(self.analyze_mortgage)

    def analyze_mortgage(self):
        """
        method for analyze mortgage

        """
        self.data.update(self.parent.mortgage_model.data)
        self.data.update(self.parent.home_model.data)

        if all(element in self.data.keys() for element in Mortgage.requirements):
            self.parent.ui.tab_widget_home.setCurrentIndex(2)

            mortgage_analysis = MortgageAnalysisProcess(self.data)
            print(mortgage_analysis.mortgage().mortgage_data)

    def clear_all(self):
        self.data = {}
