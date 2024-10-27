# -*- coding: utf-8 -*-
"""
Module containing Setting Model implementation

"""
__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

import json

from PyQt5.QtCore import QObject

from source.util import Assertor

from .model import Model


class SettingsModel(Model):
    """
    Model for Settings process

    """

    _equity_requirements = ['10 %', '15 %', '20 %', '25 %', '30%']
    _max_debt_requirements = ['4.0 x', '4.5 x', '5.0 x', '5.5 x', '6.0 x']
    _stress_test_requirements = ['3.0 %', '3.5 %', '4.0 %', '4.5 %', '5.0 %']

    def __init__(self, parent: QObject):
        """
        Constructor / Implementation

        """
        super().__init__(parent)
        Assertor.assert_data_types([parent], [QObject])
        self.parent.ui_form.combo_box_egenkapital_krav.addItems(self._equity_requirements)
        self.parent.ui_form.combo_box_gjeldsgrad.addItems(self._max_debt_requirements)
        self.parent.ui_form.combo_box_stresstest.addItems(self._stress_test_requirements)

        self.read_settings()
        self.set_combo_box("egenkapital_krav")
        self.set_combo_box("gjeldsgrad")
        self.set_combo_box("stresstest")
        self.set_settings()

    def set_settings(self):
        """
        method for setting settings in form

        """
        self.parent.ui_form.combo_box_egenkapital_krav.activated.connect(
            lambda: self.set_combo_box("egenkapital_krav"))
        self.parent.ui_form.combo_box_gjeldsgrad.activated.connect(
            lambda: self.set_combo_box("gjeldsgrad"))
        self.parent.ui_form.combo_box_stresstest.activated.connect(
            lambda: self.set_combo_box("stresstest"))

    def read_settings(self):
        """
        method for reading current settings from file

        """
        up = os.path.dirname
        settings_dir = up(up(up(__file__))) + '\\app\\processing\\engine\\tmp'

        if os.path.exists(settings_dir):
            with open(settings_dir + '\\settings.json', 'r', encoding='utf-8') as fp:
                try:
                    settings = json.load(fp)
                    self.parent.ui_form.combo_box_egenkapital_krav.setCurrentText(
                        settings['egenkapital_krav'])
                    self.parent.ui_form.combo_box_gjeldsgrad.setCurrentText(
                        settings['gjeldsgrad'])
                    self.parent.ui_form.combo_box_stresstest.setCurrentText(
                        settings['stresstest'])
                except Exception:
                    pass

    def save_settings(self):
        """
        method for saving settings in form to file

        """
        up = os.path.dirname
        settings_dir = up(up(up(__file__))) + '\\app\\processing\\engine\\tmp'

        if self.data:
            if not os.path.exists(settings_dir):
                os.makedirs(settings_dir)

            with open(settings_dir + '\\settings.json', 'w', encoding='utf-8') as fp:
                json.dump(self.data, fp)

        self.parent.close()
