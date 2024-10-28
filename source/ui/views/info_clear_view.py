# -*- coding: utf-8 -*-
"""
Info view for clearing

"""
__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
from typing import Union

from PyQt5.uic import loadUi  # pylint: disable=no-name-in-module
from PyQt5.QtGui import QIcon  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QDialog  # pylint: disable=no-name-in-module
from PyQt5.QtCore import Qt, QObject  # pylint: disable=no-name-in-module

from source.util import Assertor


class InfoClearView(QDialog):
    """
    Info dialog window

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
        up = os.path.dirname

        self.ui_form = loadUi(
            os.path.join(os.path.dirname(__file__), "forms/info_form_clear.ui"),
            self)
        self.ui_form.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui_form.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.ui_form.push_button_apply.setIcon(
            QIcon(up(up(os.path.abspath(__file__))) + '/images/check.png'))

        self.setWindowModality(Qt.ApplicationModal)
