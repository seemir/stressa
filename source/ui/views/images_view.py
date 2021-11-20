# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi

from source.util import Assertor


class ImagesView(QDialog):
    """
    Implementation of MapView

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
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "forms/images_form.ui"), self)
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
