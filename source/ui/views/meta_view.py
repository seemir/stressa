# -*- coding: utf-8 -*-

"""
Metadata Dialog which contains information of all relevant metadata

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
import json

from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi

from source.util import Assertor


class MetaView(QDialog):
    """
    MetaView with metadata information, one of several QDialog views

    """

    def __init__(self, parent: QWidget):
        """
        Constructor / Instantiation of class

        Parameters
        ----------
        parent  : QWidget
                  parent view of the metaview

        """
        Assertor.assert_data_types([parent], [QWidget])
        super().__init__(parent)
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "forms/meta_form.ui"), self)
        self.ui.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.ui.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self._parent = parent

    @property
    def parent(self):
        """
        parent getter

        Returns
        -------
        out     : QWidget
                  active parent in view

        """
        return self._parent

    def show(self):
        """
        method for showing the MetaView

        """
        try:
            metadata = self.parent.sifo_model
            self.ui.plain_text_edit_metadata.setPlainText(
                json.dumps(metadata.data, indent=2) if metadata else None)
            self.exec_()
        except Exception as metadata_error:
            self.parent.error.show_error(metadata_error)
            self.parent.error.exec_()
