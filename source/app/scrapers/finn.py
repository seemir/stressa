# -*- coding: utf-8 -*-

"""
Implementation of scarper against Finn.no housing search

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import requests

from bs4 import BeautifulSoup

from source.util import Assertor, LOGGER

from ..settings import FINN_URL
from .scraper import Scraper


class Finn(Scraper):
    """
    Scraper that scrapes housing information from Finn.no given a Finn-code

    """

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
            self._browser = requests.post((FINN_URL + "{}").format(finn_code))
            LOGGER.success(
                "created '{}', with id: [{}]".format(self.__class__.__name__, self.id_str))
        except Exception as finn_exception:
            LOGGER.exception(finn_exception)
            raise finn_exception

    def response(self):
        """
        Response from Finn-no housing search

        Returns
        -------
        our     : requests.models.Response
                  response with mortgage information

        """
        response = self._browser
        LOGGER.info("HTTP status code -> [{}: {}]".format(response.status_code, response.reason))
        return response

    def housing_information(self):
        """
        Retrieve and parse housing information from Finn.no search to dict

        Returns
        -------
        out     : dict


        """
        try:
            LOGGER.info("trying to retrieve '{}'".format(self.housing_information.__name__))
            soup = BeautifulSoup(self.response().content, "lxml")
            address = soup.find("p", attrs={"class": "u-caption"})
            if not address:
                return {}
            info = {"Adresse": address.text}
            keys, values = list(soup.find_all("dt")), list(soup.find_all("dd"))
            info.update({key.text.strip(): val.text.strip().replace(u'\xa0', ' ') for key, val in
                         zip(keys, values)})
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
            "'{}' successfully parsed to JSON at '{}'".format(self.housing_information().__name__,
                                                              file_dir))
