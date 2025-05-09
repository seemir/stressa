# -*- coding: utf-8 -*-
"""
Info view with quitting logic

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
from typing import Union

from PyQt5.uic import loadUi  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QDialog  # pylint: disable=no-name-in-module
from PyQt5.QtCore import Qt, QObject  # pylint: disable=no-name-in-module
from PyQt5.QtGui import QIcon, QPixmap  # pylint: disable=no-name-in-module

from source.util import Assertor


class InfoQuitView(QDialog):
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
            os.path.join(os.path.dirname(__file__), "forms/info_form_quit.ui"),
            self)
        self.ui_form.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui_form.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.ui_form.push_button_apply.setIcon(
            QIcon(up(up(os.path.abspath(__file__))) + '/images/check.png'))
        self.ui_form.label_info_icon.setPixmap(
            QPixmap(up(up(os.path.abspath(__file__))) + '/images/info.png'))

        self.setWindowModality(Qt.ApplicationModal)
