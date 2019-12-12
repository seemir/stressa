# -*- coding: utf-8 -*-

"""
Implementation of scarper against Finn.no housing search

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import re
from http.client import responses

import requests
from bs4 import BeautifulSoup

from source.util import cache, Assertor, LOGGER, NotFoundError, NoConnectionError

from ..settings import FINN_URL
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
                "created '{}', with id: [{}]".format(self.__class__.__name__, self.id_str))
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
            response = requests.post((FINN_URL + "{}").format(self.finn_code))
            status_code = response.status_code
            LOGGER.info("HTTP status code -> [{}: {}]".format(status_code, responses[status_code]))
            return response
        except Exception as finn_response_error:
            raise NoConnectionError(
                "Failed HTTP request - please insure that an active internet connection exists,\n"
                "exited with '{}'".format(finn_response_error))

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
            soup = BeautifulSoup(self.response().content, "lxml")

            address = soup.find("p", attrs={"class": "u-caption"}).text
            price = "".join(price.text for price in soup.find_all("span", attrs={"class": "u-t3"})
                            if " kr" in price.text).strip().replace(u"\xa0", " ")

            info = {"finn_adresse": address, "prisantydning": price}

            keys, values = list(soup.find_all(["th", "dt"])), list(soup.find_all(["td", "dd"]))
            info.update(
                {re.sub("[^a-z]+", "", key.text.lower()): val.text.strip().replace(u"\xa0", " ")
                 for key, val in zip(keys, values)})

            LOGGER.success("'{}' successfully retrieved".format(self.housing_information.__name__))
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
