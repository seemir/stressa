# -*- coding: utf-8 -*-

"""
Splash screen for the application, i.e. the first view that the viewer meets

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
import sys
import time

from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

from source.util import __version__, Assertor


class SplashView(QDialog):
    """
    Splash screen

    """

    def __init__(self, app: QApplication):
        """
        Constructor / Instantiating of class

        Parameters
        ----------
        app     : QApplication
                  main app object for which the splash screen is to be displayed

        """
        Assertor.assert_data_types([app], [QApplication])
        super().__init__()
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "forms/splash_form.ui"), self)
        self.ui.setWindowTitle(f"Stressa - v.{__version__}")
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
