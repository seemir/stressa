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

from .meta_view import MetaView


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
        dir_up = os.path.dirname

        self.ui_form = loadUi(
            os.path.join(dir_up(__file__), "forms/grunnboka_form.ui"), self)
        self.ui_form.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui_form.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.ui_form.push_button_forhandsvisning_grunnboka.setIcon(
            QIcon(dir_up(
                dir_up(os.path.abspath(__file__))) + '/images/preview.png'))

        self.download_path = dir_up(
            dir_up(os.path.abspath(__file__))) + '/util/temp'

        self._grunnboka_model = GrunnbokaModel(self)
        self.matrikkel = None
        self.postfix = None
        self.thread = None

        self._meta_view = MetaView(self)

        self.web_view = self.ui_form.web_view_grunnboka
        self.web_view.settings().setAttribute(QWebEngineSettings.PluginsEnabled,
                                              True)
        self.web_view.settings().setAttribute(
            QWebEngineSettings.PdfViewerEnabled, True)

        self.web_view.page().profile().setDownloadPath(self.download_path)
        self.web_view.page().profile().downloadRequested.connect(
            self.on_download
        )

        self.ui_form.push_button_forhandsvisning_grunnboka.clicked.connect(
            self.view_grunnboka)
        self.ui_form.push_button_metadata.clicked.connect(
            self.meta_view.display)

    def view_grunnboka(self):
        """
        method for viewing grunnboka

        """
        if 'matrikkel' + self.postfix in self.grunnboka_model.data.keys():
            if os.listdir(self.download_path):
                candidate = self.matrikkel[list(self.matrikkel.keys())[-1]]
                for file in os.listdir(self.download_path):
                    evaluator = file[-len(candidate) - 4:-4]
                    if candidate == evaluator:
                        preview_file = self.download_path + '\\' + file
                        self.web_view.load(QUrl.fromUserInput(preview_file))
                        self.web_view.show()

    def on_download(self, download):
        """
        method for handling download requests

        Parameters
        ----------
        download       : downloadRequest
                         request for download

        """
        if self.matrikkel or os.listdir(self.download_path):
            candidate = self.matrikkel[list(self.matrikkel.keys())[-1]]
            file_evaluator = [file[-len(candidate) - 4:-4] for file in
                              os.listdir(self.download_path)]
            if candidate in file_evaluator:
                for file in os.listdir(self.download_path):
                    evaluator = file[-len(candidate) - 4:-4]
                    if candidate == evaluator:
                        preview_file = self.download_path + '\\' + file
                        self.web_view.load(QUrl.fromUserInput(preview_file))
            else:
                thread = Thread(target=self.on_download_requested,
                                args=(download,))
                thread.daemon = True
                thread.start()
        else:
            self.web_view.close()

    @property
    def meta_view(self):
        """
        MetaView getter

        Returns
        -------
        out     : MetaView
                  View with the metadata for the View

        """
        return self._meta_view

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

        self.postfix = postfix
        self.grunnboka_model.add_grunnboka_data(postfix)
        if "matrikkel" + postfix in self.grunnboka_model.data.keys():
            self.matrikkel = self.grunnboka_model.data["matrikkel" + postfix]

            candidate = self.matrikkel[list(self.matrikkel.keys())[-1]]
            file_evaluator = [file[-len(candidate) - 4:-4] for file in
                              os.listdir(self.download_path)]
            if candidate in file_evaluator:
                for file in os.listdir(self.download_path):
                    evaluator = file[-len(candidate) - 4:-4]
                    if candidate == evaluator:
                        preview_file = self.download_path + '\\' + file
                        self.web_view.load(QUrl.fromUserInput(preview_file))
            else:
                kommune_nr = "0" + self.matrikkel["kommunenr"] if len(
                    self.matrikkel["kommunenr"]) == 3 else self.matrikkel[
                    "kommunenr"]
                url = "https://seeiendom.kartverket.no/eiendom/" + kommune_nr + \
                      "/" + self.matrikkel["gardsnr"] + "/" + self.matrikkel[
                          "bruksnr"] + "/0/0"
                self.web_view.setUrl(QUrl(url))
                self.web_view.show()
        else:
            self.web_view.close()

        self.show()

    def on_download_requested(self, download):
        """
        method for accepting download request

        """
        download.accept()
