# -*- coding: windows-1252 -*-

"""
Main entrance point of the application

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import sys
import traceback

from PyQt5.QtCore import QFile, QTextStream, Qt
from PyQt5.QtWidgets import QApplication

from source.ui import HomeView, SplashView, ErrorView

QApplication.setAttribute(Qt.AA_DisableHighDpiScaling, True)


class Main(QApplication):
    def __init__(self):
        super().__init__(sys.argv)

        self.f = QFile("source/ui/default_theme.qss")
        self.f.open(QFile.ReadOnly | QFile.Text)
        self.ts = QTextStream(self.f)
        self.qss = self.ts.readAll()

        self.setStyle("Fusion")
        self.setStyleSheet(self.qss)

        SplashView(self)
        self.home = HomeView()
        self.home.showMaximized()

        sys.exit(self.exec_())


def except_hook(exc_type, exc_value, exc_tb):
    error_view = ErrorView(None)
    trace_back_list = traceback.format_exception(exc_type, exc_value, exc_tb)
    trace_back = "".join(trace_back_list)
    try:
        raise Exception(
            "Error! Please contact system administrator, exited with\n'{}".format(
                trace_back_list[2])[:-2] + "''")
    except Exception as except_hook_exception:
        error_view.show_error(except_hook_exception, {}, trace_back)


if __name__ == "__main__":
    sys.excepthook = except_hook
    main = Main()
    sys.exit(main)
