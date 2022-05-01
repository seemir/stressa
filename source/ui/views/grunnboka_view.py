# -*- coding: utf-8 -*-
"""
Module with logic for the View that handles the Ownership History

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
from threading import Thread

from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import pyqtSlot, Qt, QUrl, pyqtSignal
from PyQt5.uic import loadUi

from source.util import Assertor

from ..models import GrunnbokaModel


class GrunnbokaView(QDialog):
    """
    Implementation of model for Grunnboka view

    """

    sig = pyqtSignal(int)

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
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "forms/grunnboka_form.ui"), self)
        self.ui.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self._grunnboka_model = GrunnbokaModel(self)
        self.thread = None
        self.matrikkel = None
        self.browser = self.ui.web_view_grunnboka

        up = os.path.dirname
        self.download_path = up(up(os.path.abspath(__file__))) + '/grunnboker'
        self.browser.page().profile().setDownloadPath(self.download_path)
        self.browser.page().profile().downloadRequested.connect(
            self.on_download
        )

    def on_download(self, download):
        t = Thread(target=self.on_download_requested, args=(download,))
        t.daemon = True
        t.start()

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
