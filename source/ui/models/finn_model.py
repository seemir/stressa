# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import webbrowser

from source.app import Finn

from .settings import FINN_URL
from .model import Model


class FinnModel(Model):

    def __init__(self, parent, error):
        super(FinnModel, self).__init__(parent, error)
        self._parent = parent
        self._error = error

    @property
    def data(self):
        return self._data

    def finn_info(self):
        self._parent.ui.push_button_finn_1.clicked.connect(self.open_finn_url)
        self.update_line_edits("finn_kode", self.data.keys(), Finn, "housing_information", 1)

    @staticmethod
    def open_finn_url():
        webbrowser.open(FINN_URL)
