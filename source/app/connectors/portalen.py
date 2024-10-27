# -*- coding: utf-8 -*-

"""
Implementation of connector against finansportalen.no xml feed

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import re
from http.client import responses
import xml.etree.ElementTree as Et

import requests
from requests.exceptions import ReadTimeout, ConnectionError as ConnectError

from source.util import LOGGER, NoConnectionError, TimeOutError, InvalidDataError, Tracking

from .settings import PORTALEN_URL, PORTALEN_CRED, PORTALEN_ENTRY, TIMEOUT
from .connector import Connector


class Portalen(Connector):
    """
    Connector that retrieves information from finansportalen.no mortgage XML feed

    """

    def __init__(self):
        """
        Constructor / Instantiate the class

        """
        super().__init__()
        self._browser = None
        LOGGER.success(f"created '{self.__class__.__name__}', with id: [{self.id_}]")

    @Tracking
    def portalen_response(self):
        """
        Response from finansportalen.no xml feed

        Returns
        -------
        requests.models.Response
            response with mortgage information

        """
        try:
            response = requests.get(PORTALEN_URL, auth=PORTALEN_CRED, timeout=TIMEOUT)
            status_code = response.status_code
            LOGGER.info(f"HTTP status code -> [{status_code}: {responses[status_code]}]")
            return response
        except ReadTimeout as portalen_timeout_error:
            raise TimeOutError(
                f"Timeout occurred - please try again later or contact system administrator, "
                f"exited with '{portalen_timeout_error}'"
            )
        except ConnectError as portalen_response_error:
            raise NoConnectionError(
                f"Failed HTTP request - please ensure that internet access is provided to the "
                f"client or contact system administrator, exited with '{portalen_response_error}'"
            )

    @Tracking
    def mortgage_offers(self):
        """
        Retrieve finansportalen.no's boliglån grunndata xml and returns dict for content

        Returns
        -------
        dict
            content from boliglån grunndata xml feed

        """
        LOGGER.info(f"trying to retrieve '{self.mortgage_offers.__name__}'")

        response = self.portalen_response()
        if response:
            tree = Et.fromstring(response.content.decode("windows-1252")).findall(PORTALEN_ENTRY)

            offers = {}
            count = 0

            for entries in tree:
                count += 1
                offers.update(
                    {count: {re.sub("{[^>]+}", "", entry.tag): entry.text.strip() for entry in
                             entries if entry.text}}
                )

            LOGGER.success(f"'{self.mortgage_offers.__name__}' successfully retrieved")
            return offers
        raise InvalidDataError("No 'mortgage_offers' received")

    @Tracking
    def to_json(self, file_dir: str = "report/json/mortgage_offers"):
        """
        Save mortgage offers information to JSON file

        """
        self.save_json(self.mortgage_offers(), file_dir, file_prefix="MortgageOffers_")
        LOGGER.success(f"'mortgage_offers' successfully parsed to JSON at '{file_dir}'")
