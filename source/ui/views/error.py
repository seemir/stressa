# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
import shutil
import traceback

from loguru import logger
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class PopUpError(QDialog):

    def __init__(self, parent, exception):
        super().__init__(parent)
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "error.ui"), self)
        self.ui.label_error_text.setText(str(exception))
        self.ui.plain_text_edit_traceback.setPlainText(traceback.format_exc())
        self.ui.plain_text_edit_log.setPlainText(self._read_log(exception))

    def _read_log(self, exception):
        cd = os.path.dirname(__file__)
        log_dir = os.path.join(cd, "logs")
        if os.path.exists(log_dir):
            shutil.rmtree(log_dir)
            entry = self._create_log(log_dir, exception)
        else:
            entry = self._create_log(log_dir, exception)
        return entry

    @staticmethod
    def _create_log(file_dir, exp):
        log_str = []
        file_name = "ui.log"
        error_log = logger.add(os.path.join(file_dir, file_name))
        logger.exception(exp)
        with open(os.path.join(file_dir, file_name)) as log_file:
            log_file = log_file.readlines()
        for line in log_file:
            log_str.append(line)
        logger.remove(error_log)
        return "".join(log_str)


def pop_up_error(parent, exception):
    error = PopUpError(parent, exception)
    error.exec_()
