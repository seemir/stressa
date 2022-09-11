# -*- coding: utf-8 -*-

"""
A dialog window for getting tax data from Skatteetaten

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

from typing import Union

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QObject
from PyQt5.uic import loadUi

from source.util import Assertor


class SkatteetatenView(QDialog):
    """
    Error dialog window

    """

    def __init__(self, parent: Union[QObject, None]):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        parent      : QObject
                      parent class for which this dialog window is part

        """
        Assertor.assert_data_types([parent], [(QObject, type(None))])
        super().__init__(None)
        self.ui_form = loadUi(os.path.join(os.path.dirname(__file__), "forms/skatteetaten_form.ui"),
                              self)
        self.ui_form.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui_form.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
