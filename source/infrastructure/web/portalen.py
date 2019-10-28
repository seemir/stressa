# -*- coding: utf-8 -*-

"""
Implementation of scaper against finansportalen.no xml feed

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import xml.etree.ElementTree as Et
import re
import requests
from bs4 import BeautifulSoup

from source.settings import PORTALEN_URL, PORTALEN_CRED, PORTALEN_ENTRY
from source.log import LOGGER
from .scraper import Scraper


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
            self._browser = requests.post(PORTALEN_URL, auth=PORTALEN_CRED)
            LOGGER.success(
                "created '{}', with id: [{}]".format(self.__class__.__name__, self.id_str))
        except Exception as portalen_exception:
            LOGGER.exception(portalen_exception)
            raise portalen_exception

    def response(self):
        """
        Response from finansportalen.no xml feed

        Returns
        -------
        our     : requests.models.Response
                  response with mortgage information

        """
        response = self._browser
        LOGGER.info("HTTP status code -> [{}: {}]".format(response.status_code, response.reason))
        return response

    def mortgage_offers(self):
        """
        Retrieve finansportalen.no's boliglån grunndata xml and stores it locally directory

        """
        try:
            LOGGER.info("trying to retrieve '{}'".format(self.mortgage_offers.__name__))
            offers = {}
            soup = BeautifulSoup(self.response().content.decode("windows-1252"), "xml")
            root = Et.fromstring(soup.prettify())
            remove_url_re = '{[^>]+}'
            for i, children in enumerate(root.findall(PORTALEN_ENTRY)):
                offers.update(
                    {i + 1: {re.sub(remove_url_re, '', child.tag): child.text.strip() for child in
                             children if child.text}})
            LOGGER.success("'{}' successfully retrieved".format(self.mortgage_offers.__name__))
            return offers
        except Exception as mortgage_offers_exception:
            LOGGER.exception(mortgage_offers_exception)
            raise mortgage_offers_exception

    def to_json(self, file_dir: str = "report/json/mortgage_offers"):
        """
        save mortgage offers information to JSON file

        """
        self._to_json(self.mortgage_offers(), file_dir, file_prefix="MortgageOffers_")
        LOGGER.success(
            "'{}' successfully parsed to JSON at '{}'".format(self.mortgage_offers.__name__,
                                                              file_dir))
