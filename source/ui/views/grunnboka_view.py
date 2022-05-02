# -*- coding: utf-8 -*-
"""
Module with logic for the View that handles the Ownership History

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
from threading import Thread

from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import pyqtSlot, Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineSettings

from source.util import Assertor

from ..models import GrunnbokaModel


class GrunnbokaView(QDialog):
    """
    Implementation of model for Grunnboka view

    """

    def __init__(self, parent: QWidget):
        """
        Constructor / Instantiation of class

        Parameters
        ----------
        parent  : QWidget
                  parent view of the GrunnbokaView

        """
        super().__init__(parent)
        Assertor.assert_data_types([parent], [QWidget])
        self.parent = parent
        up = os.path.dirname

        self.ui = loadUi(os.path.join(up(__file__), "forms/grunnboka_form.ui"), self)
        self.ui.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        self.download_path = up(up(os.path.abspath(__file__))) + '/grunnboker'

        self.ui.push_button_forhandsvisning_grunnboka.setIcon(
            QIcon(up(up(os.path.abspath(__file__))) + '/images/preview.png'))

        self._grunnboka_model = GrunnbokaModel(self)
        self.thread = None
        self.matrikkel = None
        self.browser = self.ui.web_view_grunnboka
        self.browser.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.browser.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)

        self.browser.page().profile().setDownloadPath(self.download_path)
        self.browser.page().profile().downloadRequested.connect(
            self.on_download
        )

        self.ui.push_button_forhandsvisning_grunnboka.clicked.connect(self.view_grunnboka)

    def view_grunnboka(self):
        if self.matrikkel or os.listdir(self.download_path):
            candidate = self.matrikkel[list(self.matrikkel.keys())[-1]]
            for file in os.listdir(self.download_path):
                evaluator = file[-len(candidate) - 4:-4]
                if candidate == evaluator:
                    preview_file = self.download_path + '\\' + file
                    self.browser.load(QUrl.fromUserInput(preview_file))
        else:
            self.browser.close()

    def on_download(self, download):
        thread = Thread(target=self.on_download_requested, args=(download,))
        thread.daemon = True
        thread.start()

    @property
    def grunnboka_model(self):
        """
        GrunnbokaModel getter

        Returns
        -------
        out     : GrunnbokaModel
                  Model containing all the logic of the GrunnbokaHistory

        """
        return self._grunnboka_model

    @pyqtSlot()
    def add_grunnboka_data(self, postfix: str):
        """
        method for adding grunnboka data to view

        Parameters
        ----------
        postfix     : str
                      index if used in naming of widgets

        """
        Assertor.assert_data_types([postfix], [str])
        self.grunnboka_model.add_grunnboka_data(postfix)
        if "matrikkel" + postfix in self.grunnboka_model.data.keys():
            self.matrikkel = self.grunnboka_model.data["matrikkel" + postfix]

            self.browser.setUrl(QUrl("https://seeiendom.kartverket.no/eiendom/0"
                                     + self.matrikkel["kommunenr"] + "/"
                                     + self.matrikkel["gardsnr"] + "/"
                                     + self.matrikkel["bruksnr"] + "/0/0"))
        self.show()

    def on_download_requested(self, download):
        download.accept()
