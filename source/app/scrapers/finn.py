# -*- coding: utf-8 -*-

"""
Implementation of scarper against Finn.no housing search

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import re
import json
from http.client import responses

import requests
from requests.exceptions import ConnectTimeout, ConnectionError as ConnectError
from bs4 import BeautifulSoup

from source.util import cache, Assertor, LOGGER, NotFoundError, NoConnectionError, TimeOutError
from source.domain import Amount

from .settings import FINN_AD_URL, FINN_STAT_URL, TIMEOUT
from .scraper import Scraper

cache(__file__, "cache")


class Finn(Scraper):
    """
    Scraper that scrapes housing information from Finn.no given a Finn-code

    """

    @staticmethod
    def validate_finn_code(finn_code: str):
        """
        static method for validating Finn.no code

        Parameters
        ----------
        finn_code    : str
                       Finn-code to be validated

        """
        valid_finn_code = re.compile("^1[0-9]{8}").search(finn_code)
        if not valid_finn_code:
            raise NotFoundError("'{}' is an invalid Finn code".format(finn_code))

    def __init__(self, finn_code: str):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        finn_code   : str
                      Finn-code to be searched for

        """
        try:
            super().__init__()
            Assertor.assert_data_types([finn_code], [str])
            self.validate_finn_code(finn_code)
            self._finn_code = finn_code
            self._browser = None
            LOGGER.success(
                "created '{}', with id: [{}]".format(self.__class__.__name__, self.id))
        except Exception as finn_exception:
            LOGGER.exception(finn_exception)
            raise finn_exception

    @property
    def finn_code(self):
        """
        Finn-kode getter

        Returns
        -------
        out     : str
                  active finn-kode in object

        """
        return self._finn_code

    def response(self):
        """
        Response from Finn-no housing search

        Returns
        -------
        our     : requests.models.Response
                  response with mortgage information

        """
        try:
            try:
                ad_response = requests.post(FINN_AD_URL + "{}".format(self.finn_code),
                                            timeout=TIMEOUT)
                stat_response = requests.post(FINN_STAT_URL + "{}".format(self.finn_code),
                                              timeout=TIMEOUT)
                ad_status_code = ad_response.status_code
                stat_status_code = stat_response.status_code
                LOGGER.info(
                    "HTTP status code -> \nAD   -> [{}: {}]"
                    "\nSTAT -> [{}: {}]".format(ad_status_code, responses[ad_status_code],
                                                stat_status_code, responses[stat_status_code]))
                return ad_response, stat_response
            except ConnectTimeout as finn_timeout_error:
                raise TimeOutError(
                    "Timeout occurred - please try again later or contact system administrator, "
                    "\nexited with '{}'".format(finn_timeout_error))
        except ConnectError as finn_response_error:
            raise NoConnectionError(
                "Failed HTTP request - please insure that internet access is provided to the "
                "client or contact system administrator,\nexited with '{}'".format(
                    finn_response_error))

    def housing_information(self):
        """
        Retrieve and parse housing information from Finn.no search to dict

        Returns
        -------
        out     : dict


        """
        try:
            LOGGER.info(
                "trying to retrieve '{}' for -> '{}'".format(self.housing_information.__name__,
                                                             self.finn_code))
            response = self.response()
            if not response:
                raise NotFoundError("'{}' is an invalid Finn code".format(self.finn_code))

            ad_soup = BeautifulSoup(response[0].content, "lxml")
            stat_soup = BeautifulSoup(response[1].content, "lxml")

            address = ad_soup.find("p", attrs={"class": "u-caption"})
            if not address:
                raise NotFoundError("'{}' is an invalid Finn code".format(self.finn_code))

            price = "".join(
                price.text for price in ad_soup.find_all("span", attrs={"class": "u-t3"})
                if " kr" in price.text).strip().replace(u"\xa0", " ")
            status = ad_soup.find("span",
                                  attrs={"class": "u-capitalize status status--warning u-mb0"})

            info = {"finn_adresse": address.text, "prisantydning": price,
                    "status": status.text.capitalize() if status else "Ikke solgt"}
            keys, values = list(ad_soup.find_all(["th", "dt"])), list(
                ad_soup.find_all(["td", "dd"]))
            info.update(
                {re.sub("[^a-z]+", "", key.text.lower()): val.text.strip().replace(u"\xa0", " ")
                 for key, val in zip(keys, values)})

            sq_price = json.loads(stat_soup.find("script", attrs={"id": "area-prices"}).text)[
                "price"]
            info.update({"sq_price": Amount.format_amount(sq_price) + " kr/m²"})
            for stat in json.loads(
                    stat_soup.find("script", attrs={"id": "ad-summary"}).text).values():
                for prop, value in stat.items():
                    info.update({prop.lower(): Amount.format_amount(value)})

            LOGGER.success(
                "'{}' successfully retrieved".format(self.housing_information.__name__))
            return info
        except Exception as housing_information_exception:
            LOGGER.exception(housing_information_exception)
            raise housing_information_exception

    def to_json(self, file_dir: str = "report/json/mortgage_offers"):
        """
        save mortgage offers information to JSON file

        """
        self.save_json(self.housing_information(), file_dir, file_prefix="HousingInfo_")
        LOGGER.success(
            "'housing_information' successfully parsed to JSON at '{}'".format(file_dir))
