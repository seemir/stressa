# -*- coding: utf-8 -*-

"""
A dialog window for getting / Importing tax data from Skatteetaten

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
import json

from typing import Union

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot, Qt, QUrl, QObject, QByteArray
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from PyQt5.QtWebEngineCore import QWebEngineHttpRequest

from source.util import Assertor

from ..models import SkatteetatenImportModel

from .meta_view import MetaView


class SkatteetatenImportView(QDialog):
    """
    Tax import model

    """

    _tax_output = ["beregnet_skatt_beloep", "beregnet_skatt_per_mnd_beloep",
                   "beregnet_skatt_foer_skattefradrag_beloep", "fellesskatt_grunnlag",
                   "fellesskatt_beloep", "fradrag_for_fagforeningskontingent", "gjeldsgrad",
                   "inntektsskatt_til_fylkeskommune_grunnlag",
                   "inntektsskatt_til_fylkeskommune_beloep", "inntektsskatt_til_kommune_grunnlag",
                   "inntektsskatt_til_kommune_beloep", "personinntekt_fra_loennsinntekt",
                   "samlet_gjeld", "samlede_paaloepte_renter_paa_gjeld_i_innenlandske_banker",
                   "samlede_opptjente_renter_i_innenlandske_banker",
                   "samlet_skattepliktig_overskudd_fra_utleie_av_fast_eiendom", "skatteklasse",
                   "skatteprosent", "skatteregnskapskommune", "sum_fradrag_i_alminnelig_inntekt",
                   "sum_inntekter_i_alminnelig_inntekt_foer_fordelingsfradrag", "sum_minstefradrag",
                   "sum_skattefradrag_beloep", "sum_trygdeavgift_grunnlag",
                   "sum_trygdeavgift_beloep", "trinnskatt_grunnlag", "trinnskatt_beloep"]

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

        self.ui_form = loadUi(
            os.path.join(os.path.dirname(__file__), "forms/skatteetaten_import_form.ui"),
            self)
        self.ui_form.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui_form.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        self.download_path = dir_up(dir_up(os.path.abspath(__file__))) + '/util/temp'

        self._meta_view = MetaView(self)

        self.web_view_primary = self.ui_form.web_view_primary
        self.web_view_secondary = self.ui_form.web_view_secondary
        self.web_view_primary.setContextMenuPolicy(Qt.NoContextMenu)
        self.web_view_primary.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.web_view_primary.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
        self.ui_form.push_button_meta_data_1.clicked.connect(self.meta_view.display)
        self.ui_form.push_button_import_tax_data_1.clicked.connect(self.import_tax_data)

        self.tax_report_url = ""
        self.tax_message_data = ""
        self.tax_result_data = ""

    @property
    def tax_output(self):
        """
        tax_output getter

        """
        return self._tax_output

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

    @pyqtSlot()
    def import_tax_data(self):
        """
        method for importing tax data to application

        """

    @pyqtSlot()
    def open_skatteetaten_page(self):
        """
        method for opening skatteetaten page

        """
        tax_url = "https://www.skatteetaten.no/globalassets/system/js/index.html?" \
                  "redirectUrl=https%3A%2F%2Fskatt.skatteetaten.no%2Fweb%2Fmineskatteforhold%2F"
        self.clear_cache()
        self.web_view_primary.setUrl(QUrl(tax_url))
        self.web_view_primary.loadFinished.connect(self.load_finished)
        self.web_view_primary.show()
        self.show()

    def load_finished(self):
        """
        method for getting auth api credentials

        """
        if self.web_view_primary.url().toString() == "https://skatt.skatteetaten.no/web/" \
                                                     "mineskatteforhold/":
            tax_api_url = "https://skatt.skatteetaten.no/api/mineskatteforhold/sider/skatt"
            tax_api_request = QWebEngineHttpRequest(QUrl.fromUserInput(tax_api_url))
            self.web_view_secondary.load(tax_api_request)
            self.web_view_secondary.loadFinished.connect(self.tax_auth_data)

    def tax_auth_data(self):
        """
        method for redirecting to tax report

        """
        self.web_view_secondary.page().toPlainText(self.show_tax_report)

    def show_tax_report(self, content):
        """
        method for displaying tax report from skatteetaten

        """
        if not self.tax_report_url and content:
            try:
                tax_data = json.loads(content)
                self.web_view_primary.setHtml('')
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
                self.web_view_primary.load(QUrl(self.tax_report_url))

                self.web_view_secondary.page().toPlainText(self.show_tax_report)

                self.tax_message_data = "https://skatt.skatteetaten.no/api/skattemeldingen/2021/" \
                                        "skattemelding/hent-gjeldende"
                self.web_view_tertiary.load(QUrl(self.tax_message_data))
                self.web_view_tertiary.loadFinished.connect(self.tax_data)

            except ValueError:
                pass

    def tax_data(self):
        """
        method for accessing tax data

        """
        self.web_view_tertiary.page().toPlainText(self.show_tax_data)

    def show_tax_data(self, content):
        """
        method for showing tax data

        """

        if content:
            payload = {"visningsdata": json.loads(content)["visningsdata"]}
            tax_result_url = "https://skatt.skatteetaten.no/api/skattemeldingen/2021/" \
                             "skattemelding/v2/beregn-og-kontroller"

            tax_api_request = QWebEngineHttpRequest()
            tax_api_request.setUrl(QUrl.fromUserInput(tax_result_url))
            tax_api_request.setMethod(QWebEngineHttpRequest.Post)
            tax_api_request.setHeader(QByteArray(b'Content-Type'), QByteArray(b'application/json'))
            tax_api_request.setPostData(bytes(json.dumps(payload).replace("'", '"'), 'utf-8'))

            self.web_view_quaternary.load(tax_api_request)
            self.web_view_quaternary.loadFinished.connect(self.tax_results)

    def tax_results(self):
        """
        method for accessing tax results

        """
        self.web_view_quaternary.page().toPlainText(self.parse_tax_results)

    def parse_tax_results(self, content):
        """
        method for parsing tax results

        """
        if content:
            full_results = tax_results = json.loads(content)

            if "skattemeldingResultat" in full_results.keys():
                if "beregnetSkatt" in full_results["skattemeldingResultat"].keys():
                    tax_results = json.loads(content)["skattemeldingResultat"]["beregnetSkatt"]
                    skatteetaten_import_model = SkatteetatenImportModel(self, tax_results)
                    skatteetaten_import_model.import_tax_results()

    def clear_cache(self):
        """
        method for clearing cache from skatteetaten pages

        """
        self.tax_report_url = ''
        self.web_view_primary.setHtml('')
        self.web_view_primary.page().profile().cookieStore().deleteAllCookies()
        self.web_view_primary.history().clear()
        self.web_view_primary.close()
