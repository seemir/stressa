# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
import json

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi


class MetaView(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "forms/meta_form.ui"), self)
        self.ui.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.ui.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self._parent = parent

    @property
    def parent(self):
        return self._parent

    def show_meta_data(self):
        try:
            metadata = self._parent.sifo_model
            self.ui.plain_text_edit_metadata.setPlainText(
                json.dumps(metadata.data, indent=2) if metadata else None)
            self.exec_()
        except Exception as metadata_error:
            self._parent.error.show_error(metadata_error)
            self._parent.error.exec_()
