# -*- coding: utf-8 -*-
"""
Implementation of scarper against Finn.no housing statistics search

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import json
from http.client import responses
import requests
from requests.exceptions import ConnectTimeout, ConnectionError as ConnectError

from bs4 import BeautifulSoup

from source.util import LOGGER, TimeOutError, NoConnectionError, NotFoundError
from source.domain import Amount

from .settings import FINN_STAT_URL, TIMEOUT
from .finn import Finn


class FinnStat(Finn):
    """
    Scraper that scrapes housing statistics information from Finn.no given a Finn-code

    """

    def __init__(self, finn_code: str):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        finn_code   : str
                      Finn-code to search finn statistics for

        """
        super().__init__(finn_code=finn_code)

    def stat_response(self):
        """
        Response from Finn-no housing statistics search

        Returns
        -------
        our     : requests.models.Response
                  response with housing statistics information

        """
        try:
            try:
                stat_response = requests.post(FINN_STAT_URL + "{}".format(self.finn_code),
                                              timeout=TIMEOUT)
                stat_status_code = stat_response.status_code
                LOGGER.info(
                    "HTTP status code -> STATISTICS: [{}: {}]".format(stat_status_code,
                                                                      responses[stat_status_code]))
                return stat_response
            except ConnectTimeout as finn_stat_timeout_error:
                raise TimeOutError(
                    "Timeout occurred - please try again later or contact system administrator, "
                    "\nexited with '{}'".format(finn_stat_timeout_error))
        except ConnectError as finn_stat_response_error:
            raise NoConnectionError(
                "Failed HTTP request - please insure that internet access is provided to the "
                "client or contact system administrator,\nexited with '{}'".format(
                    finn_stat_response_error))

    def housing_stat_information(self):
        """
        Retrieve and parse housing ad information from Finn.no search to dict

        Returns
        -------
        out     : dict


        """
        try:
            LOGGER.info(
                "trying to retrieve '{}' for -> '{}'".format(self.housing_stat_information.__name__,
                                                             self.finn_code))
            response = self.stat_response()
            if not response:
                raise NotFoundError("'{}' is an invalid Finn code".format(self.finn_code))

            stat_soup = BeautifulSoup(response.content, "lxml")

            info = {}
            sq_price = json.loads(stat_soup.find("script", attrs={"id": "area-prices"}).text)[
                "price"]
            info.update({"sqm_price": Amount.format_amount(sq_price) + " kr/m²"})

            statistics = json.loads(
                stat_soup.find("script", attrs={"id": "ad-summary"}).text)[self.finn_code]

            for prop, value in statistics.items():
                info.update({prop.lower(): Amount.format_amount(value)})

            LOGGER.success(
                "'{}' successfully retrieved".format(self.housing_stat_information.__name__))
            return info
        except Exception as housing_stat_information_exception:
            LOGGER.exception(housing_stat_information_exception)
            raise housing_stat_information_exception

    def to_json(self, file_dir: str = "report/json/finn_information"):
        """
        save mortgage offers information to JSON file

        """
        self.save_json(self.housing_stat_information(), file_dir, file_prefix="HousingStatInfo_")
        LOGGER.success(
            "'housing_stat_information' successfully parsed to JSON at '{}'".format(file_dir))
