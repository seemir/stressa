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

    def clear_all(self):
        """
        method for clearing all content in HomeView

        Returns
        -------

        """
        self.parent.ui.sifo_view.sifo_model.clear_all()
        self.parent.mortgage_model.clear_all()
        self.parent.finn_model.clear_all()
        self.parent.ui.line_edit_fornavn.setFocus()
