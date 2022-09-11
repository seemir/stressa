# -*- coding: utf-8 -*-

"""
A dialog window for getting tax data from Skatteetaten

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

from typing import Union

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot, Qt, QUrl, QObject
from PyQt5.QtWebEngineWidgets import QWebEngineSettings

from source.util import Assertor

from ..models import SkatteetatenModel

from .meta_view import MetaView


class SkatteetatenView(QDialog):
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

        self.parent = parent
        dir_up = os.path.dirname

        self.ui_form = loadUi(os.path.join(os.path.dirname(__file__), "forms/skatteetaten_form.ui"),
                              self)
        self.ui_form.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui_form.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        self.download_path = dir_up(dir_up(os.path.abspath(__file__))) + '/util/temp'

        self._skatteetaten_model = SkatteetatenModel(self)

        self._meta_view = MetaView(self)

        self.web_view = self.ui_form.web_view_primar
        self.web_view.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)

        self.ui_form.push_button_meta_data_1.clicked.connect(self.meta_view.display)

    @property
    def meta_view(self):
        """
        MetaView getter

        Returns
        -------
        out     : MetaView
                  View with the metadata for the SifoView

        """
        return self._meta_view

    @property
    def skatteetaten_model(self):
        """
        SkatteetatenModel getter

        Returns
        -------
        out     : SkatteetatenModel
                  Model containing all the logic of the SkatteetatenModel

        """
        return self._skatteetaten_model

    @pyqtSlot()
    def open_skatteetaten_page(self):
        """
        method for opening skatteetaten page

        """

        url = "https://skatt.skatteetaten.no/web/mineskatteforhold/"
        self.web_view.setUrl(QUrl(url))
        self.web_view.show()
        self.show()
