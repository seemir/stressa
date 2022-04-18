# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from PyQt5.QtCore import QObject

from source.util import Assertor

from .model import Model


class TaxModel(Model):
    _tax_year = ["", "2022", "2021", "2020", "2019", "2018"]

    def __init__(self, parent: QObject):
        super().__init__(parent)
        Assertor.assert_data_types([parent], [QObject])

        self.parent.ui.combo_box_tax_year.addItems(self.tax_year)

    @property
    def tax_year(self):
        return self._tax_year
