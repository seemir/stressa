# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.settings import portalen_url, portalen_cred, portalen_entry
import xml.etree.ElementTree as Et
from source.log import main_logger
from bs4 import BeautifulSoup
from .scraper import Scraper
import requests
import re


class Portalen(Scraper):
    """
    Scraper that scrapes information from finansportalen.no mortgage
    applications calculator

    """

    def __init__(self):
        """
        Constructor / Instantiate the class

        """
        super().__init__()
        try:
            self.browser = requests.post(portalen_url, auth=portalen_cred)
        except Exception as exp:
            main_logger.exception(exp)
            raise exp
        main_logger.success(
            "created scraper: '{}', with id: [{}]".format(self.__class__.__name__, self.id))

    def response(self):
        """
        Response from finansportalen.no xml feed

        Returns
        -------
        our     : requests.models.Response
                  response with mortgage information

        """
        return self.browser

    def mortgage_offers(self):
        """
        Retrieve finansportalen.no's boliglån grunndata xml and stores it locally directory

        """
        try:
            offers = {}
            soup = BeautifulSoup(self.response().content.decode("windows-1252"), "xml")
            root = Et.fromstring(soup.prettify())
            remove_url_re = '{[^>]+}'
            for i, children in enumerate(root.findall(portalen_entry)):
                offers.update(
                    {i + 1: {re.sub(remove_url_re, '', child.tag): child.text.strip() for child in
                             children if child.text}})
        except Exception as exp:
            main_logger.exception(exp)
            raise exp
        return offers

    def to_json(self, file_dir: str = "report/json/mortgage_offers"):
        """
        save mortgage offers information to JSON file

        """
        self._to_json(self.mortgage_offers(), file_dir, file_title="MortgageOffers_")
