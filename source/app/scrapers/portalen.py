# -*- coding: utf-8 -*-

"""
Implementation of scaper against finansportalen.no xml feed

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import gc
import re
from http.client import responses
import xml.etree.ElementTree as Et

import requests
from bs4 import BeautifulSoup

from source.util import LOGGER, cache

from ..settings import PORTALEN_URL, PORTALEN_CRED, PORTALEN_ENTRY
from .scraper import Scraper

cache(__file__, "cache")


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
        self._browser = None
        LOGGER.success(
            "created '{}', with id: [{}]".format(self.__class__.__name__, self.id_str))

    @staticmethod
    def response():
        """
        Response from finansportalen.no xml feed

        Returns
        -------
        our     : requests.models.Response
                  response with mortgage information

        """
        response = requests.post(PORTALEN_URL, auth=PORTALEN_CRED)
        status_code = response.status_code
        LOGGER.info("HTTP status code -> [{}: {}]".format(status_code, responses[status_code]))
        return response

    def mortgage_offers(self):
        """
        Retrieve finansportalen.no's boliglån grunndata xml and returns dict for content

        Returns
        -------
        out     : dict
                  content from boliglån grunndata Xxml feed

        """
        try:
            LOGGER.info("trying to retrieve '{}'".format(self.mortgage_offers.__name__))

            offers = {}
            soup = BeautifulSoup(self.response().content.decode("windows-1252"), "xml")
            tree = Et.fromstring(soup.prettify()).findall(PORTALEN_ENTRY)

            for i, entries in enumerate(tree):
                offers[i + 1] = {re.sub("{[^>]+}", "", entry.tag): entry.text.strip() for entry in
                                 entries if entry.text}
            gc.collect()

            LOGGER.success("'{}' successfully retrieved".format(self.mortgage_offers.__name__))
            return offers
        except Exception as mortgage_offers_exception:
            LOGGER.exception(mortgage_offers_exception)
            raise mortgage_offers_exception

    def to_json(self, file_dir: str = "report/json/mortgage_offers"):
        """
        save mortgage offers information to JSON file

        """
        self.save_json(self.mortgage_offers(), file_dir, file_prefix="MortgageOffers_")
        LOGGER.success("'mortgage_offers' successfully parsed to JSON at '{}'".format(file_dir))
