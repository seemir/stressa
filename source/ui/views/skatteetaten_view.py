# -*- coding: utf-8 -*-

"""
A dialog window for getting tax data from Skatteetaten

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
import json

from typing import Union

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot, Qt, QUrl, QObject
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from PyQt5.QtWebEngineCore import QWebEngineHttpRequest

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
        self.web_view.setContextMenuPolicy(Qt.NoContextMenu)
        self.web_view.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
        self.ui_form.push_button_meta_data_1.clicked.connect(self.meta_view.display)
        self.ui_form.push_button_import_tax_data_1.clicked.connect(self.import_tax_data)

        self.tax_report_url = ''
        self.tax_message_data = ''

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
    def import_tax_data(self):
        """
        method for importing tax data to application

        """
        if self.tax_report_url:
            prelim_tax_url = 'https://skatt.skatteetaten.no/api/skattemeldingen/2021/' \
                             'skattemelding/hent-gjeldende'
            self.web_view.setHtml('')
            self.web_view.setUrl(QUrl(prelim_tax_url))

    @pyqtSlot()
    def open_skatteetaten_page(self):
        """
        method for opening skatteetaten page

        """
        tax_url = "https://www.skatteetaten.no/globalassets/system/js/index.html?" \
                  "redirectUrl=https%3A%2F%2Fskatt.skatteetaten.no%2Fweb%2Fmineskatteforhold%2F"
        self.clear_cache()
        self.web_view.setUrl(QUrl(tax_url))
        self.web_view.loadFinished.connect(self.load_finished)
        self.web_view.show()
        self.show()

    def load_finished(self):
        """
        method for getting auth api credentials

        """
        if self.web_view.url().toString() == "https://skatt.skatteetaten.no/web/mineskatteforhold/":
            tax_api_url = "https://skatt.skatteetaten.no/api/mineskatteforhold/sider/skatt"
            tax_api_request = QWebEngineHttpRequest(QUrl.fromUserInput(tax_api_url))
            self.web_view.load(tax_api_request)
            self.web_view.loadFinished.connect(self.tax_auth_data)

    def tax_auth_data(self):
        """
        method for redirecting to tax report

        """
        self.web_view.page().toPlainText(self.show_tax_report)

    def show_tax_report(self, content):
        """
        method for displaying tax report from skatteetaten

        """
        if not self.tax_report_url and content:
            try:
                tax_data = json.loads(content)
                self.web_view.setHtml('')
                document_id = ''
                if "blokker" in tax_data.keys():
                    for blokk in tax_data["blokker"]:
                        if "blokknavn" in blokk.keys():
                            if blokk["blokknavn"] == "historikk":
                                if "blokker" in blokk.keys():
                                    for sub_blokk in blokk["blokker"]:
                                        if "blokknavn" in sub_blokk.keys():
                                            if sub_blokk["blokknavn"] == \
                                                    'historikk-skatteoppgjoer_2021':
                                                if "blokkdata" in sub_blokk.keys():
                                                    if "data" in sub_blokk["blokkdata"].keys():
                                                        sub_blokk_data = sub_blokk["blokkdata"][
                                                            "data"]
                                                        if "dokumentId" in sub_blokk_data:
                                                            document_id = sub_blokk_data[
                                                                "dokumentId"]
                self.tax_report_url = "https://skatt.skatteetaten.no/api/mineskatteforhold/" \
                                      "dokumentregister/{}/skatteoppgjoer_personlig_v1/" \
                                      "?aar=2021".format(document_id)
                self.web_view.load(QUrl(self.tax_report_url))
            except ValueError:
                pass

    def clear_cache(self):
        """
        method for clearing cache from skatteetaten pages

        """
        self.tax_report_url = ''
        self.web_view.setHtml('')
        self.web_view.page().profile().cookieStore().deleteAllCookies()
        self.web_view.history().clear()
        self.web_view.close()
