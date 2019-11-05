# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from source.app import Posten
from source.domain import Phone

from .error import pop_up_error
from . import resources


class HomePage(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "home.ui"), self)
        self.ui.combo_box_gender.addItems(["", "Mann", "Kvinne"])

        self.ui.line_edit_zip_code.editingFinished.connect(self.update_post_code_info)

        self.ui.line_edit_mobile_phone.editingFinished.connect(
            lambda: self.format_phone_number("mobile_phone"))
        self.ui.line_edit_private_phone.editingFinished.connect(
            lambda: self.format_phone_number("private_phone"))
        self.ui.line_edit_work_phone.editingFinished.connect(
            lambda: self.format_phone_number("work_phone"))

    def update_post_code_info(self):
        line_edits = ["city", "municipality", "county"]
        zip_code = self.ui.line_edit_zip_code
        try:
            zip_code_str = zip_code.text().strip()
            if zip_code_str:
                posten = Posten(zip_code_str)
                zip_code_info = posten.zip_code_info()
                for line_edit in line_edits:
                    getattr(self.ui, "line_edit_" + line_edit).setText(zip_code_info[line_edit])
            else:
                zip_code.clear()
                for line_edit in line_edits:
                    getattr(self.ui, "line_edit_" + line_edit).clear()
        except Exception as post_error:
            pop_up_error(self, post_error)
            zip_code.clear()
            for line_edit in line_edits:
                getattr(self.ui, "line_edit_" + line_edit).clear()

    def format_phone_number(self, name: str):
        line_edit = getattr(self.ui, "line_edit_" + name)
        line_edit_str = line_edit.text().strip()
        try:
            if line_edit_str:
                phone = Phone(line_edit_str)
                line_edit.setText(phone.format_number())
            else:
                line_edit.clear()
        except Exception as phone_error:
            pop_up_error(self, phone_error)
            line_edit.clear()
