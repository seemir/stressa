# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

from .error import Error
from . import resources

from ..models import Formatting


class SifoCalc(QDialog):

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "forms/sifo_calc.ui"), self)
        self._formatting = Formatting(self, Error)

        self._formatting.format_sifo_info(self.parent)
