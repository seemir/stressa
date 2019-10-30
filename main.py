# -*- coding: windows-1252 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import sys

from PyQt5 import QtWidgets

from source.ui.views import HomePage

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = HomePage()
    application.show()
    sys.exit(app.exec())
