# -*- coding: utf-8 -*-
"""
Implementation of scarper against Finn.no housing ad search

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from time import time
import re
from http.client import responses
import requests
from requests.exceptions import ConnectTimeout, ConnectionError as ConnectError

from bs4 import BeautifulSoup

from source.util import LOGGER, TimeOutError, NoConnectionError, NotFoundError, Assertor

from .settings import FINN_AD_URL, TIMEOUT
from .finn import Finn


class FinnAd(Finn):
    """
    Scraper that scrapes housing ad information from Finn.no given a Finn-code

    """

    def __init__(self, finn_code: str):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        finn_code   : str
                      Finn-code to be search finn-ad information

        """
        Assertor.assert_data_types([finn_code], [str])
        super().__init__(finn_code=finn_code)

    def ad_response(self):
        """
        Response from Finn-no ad housing search

        Returns
        -------
        our     : requests.models.Response
                  response with housing ad information

        """
        try:
            try:
                start = time()
                ad_response = requests.get(FINN_AD_URL + "{}".format(self.finn_code),
                                           timeout=TIMEOUT)
                ad_status_code = ad_response.status_code
                elapsed = self.elapsed_time(start)
                LOGGER.info(
                    "HTTP status code -> ADVERT: [{}: {}] -> elapsed: {}".format(
                        ad_status_code, responses[ad_status_code], elapsed))
                return ad_response
            except ConnectTimeout as finn_ad_timeout_error:
                raise TimeOutError(
                    "Timeout occurred - please try again later or contact system administrator, "
                    "\nexited with '{}'".format(finn_ad_timeout_error))
        except ConnectError as finn_ad_response_error:
            raise NoConnectionError(
                "Failed HTTP request - please insure that internet access is provided to the "
                "client or contact system administrator,\nexited with '{}'".format(
                    finn_ad_response_error))

    def housing_ad_information(self):
        """
        Retrieve and parse housing ad information from Finn.no search to dict

        Returns
        -------
        out     : dict


        """
        try:
            try:
                LOGGER.info(
                    "trying to retrieve '{}' for -> '{}'".format(
                        self.housing_ad_information.__name__,
                        self.finn_code))
                response = self.ad_response()
                if not response:
                    raise NotFoundError(
                        "Not found! '{}' may be an invalid Finn code".format(self.finn_code))

                ad_soup = BeautifulSoup(response.content, "lxml")
                address = ad_soup.find("p", attrs={"class": "u-caption"})

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

                LOGGER.success(
                    "'{}' successfully retrieved".format(self.housing_ad_information.__name__))
                return info
            except AttributeError as no_housing_ad_information_exception:
                raise NotFoundError("Not enough advert information found, exited with '{}'".format(
                    no_housing_ad_information_exception))
        except Exception as housing_ad_information_exception:
            LOGGER.exception(housing_ad_information_exception)
            raise housing_ad_information_exception

    def to_json(self, file_dir: str = "report/json/finn_information"):
        """
        save advert information to JSON file

        """
        Assertor.assert_data_types([file_dir], [str])
        self.save_json(self.housing_ad_information(), file_dir, file_prefix="HousingAdInfo_")
        LOGGER.success(
            "'housing_ad_information' successfully parsed to JSON at '{}'".format(file_dir))
