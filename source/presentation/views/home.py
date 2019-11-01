# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

from PyQt5 import QtWidgets
from PyQt5.uic import loadUi

from source.application import Posten

from . import resources


class HomePage(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = loadUi(os.path.dirname(__file__) + "/home.ui", self)
        self.ui.combo_box_gender.addItems(["", "Mann", "Kvinne"])
        self.ui.line_edit_zip_code.editingFinished.connect(self.update_post_code_info)

    def update_post_code_info(self):
        try:
            posten = Posten(self.ui.line_edit_zip_code.text())
            zip_code_info = posten.zip_code_info()
            self.ui.line_edit_city.setText(zip_code_info["city"])
            self.ui.line_edit_municipality.setText(zip_code_info["municipality"].rsplit(' ', 1)[0])
            self.ui.line_edit_county.setText(zip_code_info["county"])
        except Exception:
            self.ui.line_edit_city.setText("")
            self.ui.line_edit_municipality.setText("")
            self.ui.line_edit_county.setText("")
