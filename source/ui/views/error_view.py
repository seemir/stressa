# -*- coding: utf-8 -*-

"""
A dialog window that gets show whenever an error occurs. Information from the traceback, log and
metadata gets populated in the window for the viewer to examine.

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
import shutil
import traceback
import json

from typing import Union
import time

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot, Qt, QObject
from PyQt5.uic import loadUi
from loguru import logger

from source.util import Assertor


class ErrorView(QDialog):
    """
    Error dialog window

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
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "forms/error_form.ui"), self)
        self.ui.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.log_dir = os.path.join(os.path.dirname(__file__), "logs")

    def show_error(self, exception: Exception, meta: dict, trace_back=None):
        """
        method for shows an error form with exception, traceback and log information

        Parameters
        ----------
        exception   : Exception
                      exception to be added to form
        meta        : dict
                      metadata
        trace_back  : str, optional
                      Optional trace_back string

        """
        time.sleep(0.2)
        if os.path.exists(self.log_dir):
            shutil.rmtree(self.log_dir)
        Assertor.assert_data_types([exception, meta], [Exception, dict])
        self.ui.tab_widget_error.setCurrentIndex(0)
        error_list = str(exception).split("->")
        error = error_list[-1].strip()
        tracking = []
        for i, element in enumerate(error_list):
            if i == 0:
                tracking.append(element + "\n")
            else:
                tracking.append("|\n")
                tracking.append("|" + "__" * i * 2 + element + "\n")

        self.ui.label_error_text.setText(error)
        self.ui.plain_text_edit_tracking.setPlainText("".join(tracking))
        self.ui.plain_text_edit_traceback.setPlainText(
            traceback.format_exc() if not trace_back else trace_back)
        self.ui.plain_text_edit_log.setPlainText(self.read_log(exception))
        self.ui.plain_text_edit_error_meta_data.setPlainText(
            json.dumps(meta, indent=4, ensure_ascii=False))
        self.show()

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
        Assertor.assert_data_types([exception], [Exception])
        return self.extract_log(self.log_dir, exception)

    @staticmethod
    def extract_log(file_dir: str, exp: Exception):
        """
        static method for creating temp log file and extracting details from this file,
        for details about content, see app.log

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
        Assertor.assert_data_types([file_dir, exp], [str, Exception])
        log_str = []
        file_name = "ui.log"
        error_log = logger.add(os.path.join(file_dir, file_name))
        logger.exception(exp)
        with open(os.path.join(file_dir, file_name)) as log_file:
            for lines in log_file.readlines():
                log_str.append(lines)
            logger.remove(error_log)
            log_file.close()
        return "".join(log_str)
