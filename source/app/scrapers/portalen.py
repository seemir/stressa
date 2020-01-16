# -*- coding: utf-8 -*-

"""
Implementation of scaper against finansportalen.no xml feed

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import re
from http.client import responses
import xml.etree.cElementTree as Et

import requests
from requests.exceptions import ReadTimeout, ConnectionError as ConnectError

from source.util import LOGGER, cache, NoConnectionError, TimeOutError, NotFoundError

from .settings import PORTALEN_URL, PORTALEN_CRED, PORTALEN_ENTRY, TIMEOUT
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
        try:
            try:
                response = requests.post(PORTALEN_URL, auth=PORTALEN_CRED, timeout=TIMEOUT)
                status_code = response.status_code
                LOGGER.info(
                    "HTTP status code -> [{}: {}]".format(status_code, responses[status_code]))
                return response
            except ReadTimeout as portalen_timeout_error:
                raise TimeOutError(
                    "Timeout occurred - please try again later or contact system administrator, "
                    "\nexited with '{}'".format(portalen_timeout_error))
        except ConnectError as portalen_response_error:
            raise NoConnectionError(
                "Failed HTTP request - please insure that internet access is provided to the "
                "client or contact system administrator,\nexited with '{}'".format(
                    portalen_response_error))

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

            response = self.response()
            if response:
                tree = Et.fromstring(response.content.decode("windows-1252")).findall(
                    PORTALEN_ENTRY)

                offers = {}
                count = 0

                for entries in tree:
                    count += 1
                    offers.update(
                        {count: {re.sub("{[^>]+}", "", entry.tag): entry.text.strip() for entry in
                                 entries if entry.text}})

                LOGGER.success("'{}' successfully retrieved".format(self.mortgage_offers.__name__))
                return offers
            raise NotFoundError("No 'mortgage_offers' received")
        except Exception as mortgage_offers_exception:
            LOGGER.exception(mortgage_offers_exception)
            raise mortgage_offers_exception

    def to_json(self, file_dir: str = "report/json/mortgage_offers"):
        """
        save mortgage offers information to JSON file

        """
        self.save_json(self.mortgage_offers(), file_dir, file_prefix="MortgageOffers_")
        LOGGER.success("'mortgage_offers' successfully parsed to JSON at '{}'".format(file_dir))
