# -*- coding: utf-8 -*-
"""
Implementation of scarper against Finn.no housing ownership history search

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from time import time
from http.client import responses
import requests
from requests.exceptions import ConnectTimeout, ConnectionError as ConnectError

from bs4 import BeautifulSoup
from pandas import DataFrame

from source.util import LOGGER, TimeOutError, NoConnectionError

from .settings import FINN_OWNER_URL, TIMEOUT
from .finn import Finn


class FinnOwnership(Finn):
    """
    Scraper that scrapes housing ownership history from Finn.no given a Finn-code

    """

    def __init__(self, finn_code: str):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        finn_code   : str
                      Finn-code to search finn ownership history information for

        """
        super().__init__(finn_code=finn_code)

    def ownership_response(self):
        """
        Response from Finn-no housing ownership history search

        Returns
        -------
        our     : requests.models.Response
                  response with housing ownership information

        """
        try:
            try:
                start = time()
                owner_response = requests.get(FINN_OWNER_URL + "{}".format(self.finn_code),
                                              timeout=TIMEOUT)
                owner_status_code = owner_response.status_code
                elapsed = self.elapsed_time(start)
                LOGGER.info(
                    "HTTP status code -> OWNERSHIP HISTORY: [{}: {}] -> elapsed: {}".format(
                        owner_status_code, responses[owner_status_code], elapsed))
                return owner_response
            except ConnectTimeout as finn_owner_timeout_error:
                raise TimeOutError(
                    "Timeout occurred - please try again later or contact system administrator, "
                    "\nexited with '{}'".format(finn_owner_timeout_error))
        except ConnectError as finn_owner_response_error:
            raise NoConnectionError(
                "Failed HTTP request - please insure that internet access is provided to the "
                "client or contact system administrator,\nexited with '{}'".format(
                    finn_owner_response_error))

    def housing_ownership_information(self):
        """
        Retrieve and parse housing ownership history information from Finn.no search to dict

        Returns
        -------
        out     : dict


        """
        try:
            LOGGER.info(
                "trying to retrieve '{}' for -> '{}'".format(
                    self.housing_ownership_information.__name__, self.finn_code))
            history_headers = None
            history_results = []
            keys = []
            values = []
            try:
                owner_soup = BeautifulSoup(self.ownership_response().content, "lxml")
                for geo_val in owner_soup.find_all("dl", attrs={"class": "definition-list u-mb32"}):
                    for i, val in enumerate(geo_val.text.split("\n")):
                        if i % 2 != 0 and val:
                            keys.append(val.strip().lower().replace("å", "a"))
                        elif val:
                            values.append(val.strip())

                for table_row in owner_soup.find(
                        "table", attrs={"class": "data-table u-mb32"}).find_all("tr"):
                    if not history_headers:
                        history_headers = [head.text for head in table_row.find_all("th")]
                    row = [tab_row.text.strip().replace(",-", " kr") for tab_row in
                           table_row.find_all("td") if tab_row.text.strip()]
                    if row:
                        history_results.append(row)

                info = dict(zip(keys, values))
                historic_df = DataFrame(history_results, columns=history_headers)
                info.update(
                    {"historikk": historic_df.assign(Pris=historic_df.iloc[:, -1].str.replace(
                        ",", " kr").str.replace("\u2212", "")).to_dict()})

                LOGGER.success(
                    "'{}' successfully retrieved".format(
                        self.housing_ownership_information.__name__))
                return info
            except AttributeError as no_ownership_history_exception:
                LOGGER.debug("No ownership history found!, exited with '{}'".format(
                    no_ownership_history_exception))
        except Exception as housing_owner_information_exception:
            LOGGER.exception(housing_owner_information_exception)
            raise housing_owner_information_exception

    def to_json(self, file_dir: str = "report/json/finn_information"):
        """
        save ownership information to JSON file

        """
        self.save_json(self.housing_ownership_information(), file_dir,
                       file_prefix="HousingOwnershipInfo_")

        LOGGER.success(
            "'housing_ownership_information' successfully parsed to JSON at '{}'".format(file_dir))
