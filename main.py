# -*- coding: windows-1252 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import sys

import qdarkstyle
from PyQt5.QtWidgets import QApplication

from source.ui import HomeView, SplashView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5()) # dark theme
    splash = SplashView(app)
    application = HomeView()
    application.show()
    sys.exit(app.exec_())
