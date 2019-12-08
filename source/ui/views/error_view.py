# -*- coding: utf-8 -*-

"""
A dialog window that gets show whenever a error occurs. Information from the traceback
and log gets populated in the window for the viewer to examine.

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
import shutil
import traceback

from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import pyqtSlot
from PyQt5.uic import loadUi
from loguru import logger


class ErrorView(QDialog):
    """
    Error dialog window

    """

    def __init__(self, parent: QWidget):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        parent      : QWidget
                      parent class for which this dialog window is part

        """
        super().__init__(parent)
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "forms/error_form.ui"), self)

    def show_error(self, exception):
        """
        method for shows an error form with exception, traceback and log information

        Parameters
        ----------
        exception   : Exception
                      exception to be added to form

        """
        self.ui.label_error_text.setText(str(exception))
        self.ui.plain_text_edit_traceback.setPlainText(traceback.format_exc())
        self.ui.plain_text_edit_log.setPlainText(self.read_log(exception))

    @pyqtSlot()
    def read_log(self, exception: Exception):
        """
        method that reads from log file the exception details

        Parameters
        ----------
        exception   : Exception
                      exception to be read

        Returns
        -------
        out         : str
                      details about exception from log

        """
        log_dir = os.path.join(os.path.dirname(__file__), "logs")
        return self.extract_log(log_dir, exception)

    @staticmethod
    def extract_log(file_dir: str, exp: Exception):
        """
        static method for creating temp log file and extracting details from this file.
        keep in mind that the log file gets deleted automatically ones the message has been
        populated to the view. for details about content, see app.log

        Parameters
        ----------
        file_dir    : str
                      name of file directory to create temp log file
        exp         : Exception
                      the exception to extract from log file

        Returns
        -------
        out         : str
                      log details about exception

        """
        log_str = []
        file_name = "ui.log"
        if os.path.exists(file_dir):
            shutil.rmtree(file_dir)
        error_log = logger.add(os.path.join(file_dir, file_name))
        logger.exception(exp)
        with open(os.path.join(file_dir, file_name)) as log_file:
            for lines in log_file.readlines():
                log_str.append(lines)
        logger.remove(error_log)
        shutil.rmtree(file_dir)
        return "".join(log_str)
