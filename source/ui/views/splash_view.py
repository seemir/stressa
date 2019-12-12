# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
import time

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class SplashView(QDialog):

    def __init__(self, app):
        super(SplashView, self).__init__()
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "forms/splash_form.ui"), self)
        self.ui.progress_bar_splash.setStyleSheet(self.change_color())

        self.show()
        for i in range(1, self.ui.progress_bar_splash.maximum() + 1):
            self.ui.progress_bar_splash.setValue(i)
            t = time.time()
            while time.time() < t + 0.1:
                app.processEvents()
        self.close()

    @staticmethod
    def change_color():
        return """QProgressBar::chunk { background: #4c96d7; width: 10px; margin: 1px; }"""
