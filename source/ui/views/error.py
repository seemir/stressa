# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
import shutil
import traceback

from loguru import logger
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class Error(QDialog):

    def __init__(self, parent, exception):
        super().__init__(parent)
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "forms/error.ui"), self)
        self.ui.label_error_text.setText(str(exception))
        self.ui.plain_text_edit_traceback.setPlainText(traceback.format_exc())
        self.ui.plain_text_edit_log.setPlainText(self.read_log(exception))

    def read_log(self, exception):
        log_dir = os.path.join(os.path.dirname(__file__), "logs")
        return self.extract_log(log_dir, exception)

    @staticmethod
    def extract_log(file_dir, exp):
        log_str = []
        file_name = "ui.log"
        error_log = logger.add(os.path.join(file_dir, file_name))
        logger.exception(exp)
        with open(os.path.join(file_dir, file_name)) as log_file:
            for lines in log_file.readlines():
                log_str.append(lines)
        logger.remove(error_log)
        shutil.rmtree(file_dir)
        return "".join(log_str)
