# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

from source.ui.models import SifoModel

from . import resources


class SifoView(QDialog):

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "forms/sifo_form.ui"), self)
        self._parent = parent
        self._sifo_model = SifoModel(self, self._parent.error)

    @property
    def parent(self):
        return self._parent

    def sifo_calculation(self):
        self._parent.ui.push_button_sifo_utgifter.clicked.connect(self._sifo_model.sifo_info)
