# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi

from source.ui.models import SifoModel

from .meta_view import MetaView

from . import resources


class SifoView(QDialog):

    def __init__(self, parent):
        super(SifoView, self).__init__(parent=parent)
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "forms/sifo_form.ui"), self)
        self.ui.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.ui.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self._parent = parent
        self._sifo_model = SifoModel(self)
        self._error = self._parent.error
        self._meta_view = MetaView(self)
        self.ui.push_button_metadata.clicked.connect(self._meta_view.show)

    @property
    def sifo_model(self):
        return self._sifo_model

    @property
    def meta_view(self):
        return self._meta_view

    @property
    def parent(self):
        return self._parent

    @property
    def error(self):
        return self._error

