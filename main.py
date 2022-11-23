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
from source.util import LOGGER

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


class Main(QApplication):
    """
    Implementation of the main application class

    """

    def __init__(self):
        """
        Constructor / Instantiate the class

        """
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
    """
    exception hook to handle all exception that are handled by logic in the application

    """
    error_view = ErrorView(None)
    trace_back_list = [trace.strip() + "\n" for trace in
                       traceback.format_exception(exc_type, exc_value, exc_tb)]
    trace_back = "".join(trace_back_list)
    try:
        raise Exception(
            "Error! Please contact system administrator, exited with\n\n'{}: {}'".format(
                exc_type.__name__, exc_value))
    except Exception as except_hook_exception:
        error_view.show_error(except_hook_exception, {}, trace_back)
        LOGGER.exception("{}\n\n {}".format(except_hook_exception, trace_back.strip()))


if __name__ == "__main__":
    sys.excepthook = except_hook
    main = Main()
    sys.exit(main)
