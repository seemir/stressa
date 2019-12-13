# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
import sys
import time

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

from source.util import __version__


class SplashView(QDialog):

    def __init__(self, app):
        super(SplashView, self).__init__()
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "forms/splash_form.ui"), self)
        self.ui.progress_bar_splash.setStyleSheet(self.change_color())
        self.ui.setWindowTitle("Stressa - version: {}".format(__version__))
        self.ui.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.app = app

        self.show()
        for i in range(1, self.ui.progress_bar_splash.maximum() + 1):
            if not self.isVisible():
                sys.exit(-1)
            self.ui.progress_bar_splash.setValue(i)
            t = time.time()
            while time.time() < t + 0.1:
                self.app.processEvents()
        self.close()

    @staticmethod
    def change_color():
        return """QProgressBar::chunk { background: #4c96d7; width: 10px; margin: 1px; }"""
