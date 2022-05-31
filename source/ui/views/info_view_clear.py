# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
from typing import Union

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.uic import loadUi

from source.util import Assertor


class InfoViewClear(QDialog):
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

        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "forms/info_form_clear.ui"), self)
        self.ui.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.ui.push_button_apply.setIcon(
            QIcon(up(up(os.path.abspath(__file__))) + '/images/check.png'))
        self.ui.label_info_icon.setPixmap(
            QPixmap(up(up(os.path.abspath(__file__))) + '/images/info.png'))

        self.setWindowModality(Qt.ApplicationModal)
