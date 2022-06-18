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

    _analysis_keys = ['arsinntekt_aar', 'belaning', 'belaningsgrad', 'egenkapital_2',
                      'egenkapital_andel', 'netto_likviditet_2', 'total_ramme', 'krav_belaning',
                      'krav_egenkapital_andel', 'krav_belaningsgrad', 'krav_total_ramme',
                      'krav_egenkapital', 'stresstest_annuitet', 'stresstest_serie',
                      'krav_stresstest_annuitet', 'krav_stresstest_serie']

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

    @property
    def analysis_keys(self):
        """
        analysis keys getter

        """
        return self._analysis_keys

    def analyze_mortgage(self):
        """
        method for analyze mortgage

        """
        self.data.update(self.parent.budget_model.data)
        self.data.update(self.parent.mortgage_model.data)
        self.data.update(self.parent.home_model.data)

        if all(element in self.data.keys() for element in Mortgage.requirements):
            self.parent.ui.tab_widget_home.setCurrentIndex(2)

            mortgage_analysis = MortgageAnalysisProcess(self.data)
            self.set_line_edits(line_edit_text='', line_edits=self.analysis_keys,
                                data=mortgage_analysis.mortgage())

    def clear_all(self):
        self.data = {}
        self.clear_line_edits(self.analysis_keys)
