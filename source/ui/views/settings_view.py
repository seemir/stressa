# -*- coding: utf-8 -*-
"""
Settings view with settings logic

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
from typing import Union

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QObject
from PyQt5.uic import loadUi

from source.util import Assertor

from ..models import SettingsModel

from .meta_view import MetaView


class SettingsView(QDialog):
    """
    Settings dialog window

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
        self.ui_form = loadUi(os.path.join(os.path.dirname(__file__), "forms/settings_form.ui"),
                              self)
        self.ui_form.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui_form.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.setWindowModality(Qt.ApplicationModal)

        self._meta_view = MetaView(self)

        self._settings_model = SettingsModel(self)
        self.ui_form.push_button_metadata.clicked.connect(self.meta_view.display)
        self.ui_form.push_button_lagre.clicked.connect(self.settings_model.save_settings)

    @property
    def settings_model(self):
        """
        SettingsModel getter

        Returns
        -------
        out     : SettingsModel
                  Model with the data on Model for View

        """
        return self._settings_model

    @property
    def meta_view(self):
        """
        MetaView getter

        Returns
        -------
        out     : MetaView
                  View with the metadata for the View

        """
        return self._meta_view
