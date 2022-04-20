# -*- coding: utf-8 -*-

"""
Module with the logic of the Home model

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from PyQt5.QtCore import QObject

from source.util import Assertor

from .model import Model


class HomeModel(Model):
    """
    Implementation of the Home model logic

    """

    def __init__(self, parent):
        super().__init__(parent)
        Assertor.assert_data_types([parent], [QObject])
        self.data = self.parent.meta_view.get_all_meta_data()

    def clear_all(self):
        """
        method for clearing all content in HomeView

        Returns
        -------

        """
        self.parent.mortgage_model.clear_all()
        self.parent.budget_view.clear_all()
        self.parent.tax_view.clear_all()
        self.parent.sifo_view.clear_all()
        self.parent.finn_model.clear_all()

        self.parent.ui.line_edit_fornavn_2.setFocus()
        self.parent.ui.tab_widget_lanesokere.setCurrentIndex(0)
        self.parent.ui.line_edit_fornavn_1.setFocus()
