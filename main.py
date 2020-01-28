# -*- coding: windows-1252 -*-

"""
Main entrance point of the application

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import sys

from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QApplication

from source.ui import HomeView, SplashView

if __name__ == "__main__":
    f = QFile("source/ui/dark_theme.qss")
    f.open(QFile.ReadOnly | QFile.Text)
    ts = QTextStream(f)
    qss = ts.readAll()

    app = QApplication(sys.argv)
    # app.setStyleSheet(qss)
    splash = SplashView(app)
    application = HomeView()
    application.showMaximized()
    sys.exit(app.exec_())
