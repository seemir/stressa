# -*- coding: utf-8 -*-
"""
Module containing logic for scraper against "nabolag" profiles of Finn ad

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from time import time

import json
from http.client import responses

from requests.exceptions import ConnectTimeout, ConnectionError as ConnectError
import requests

from bs4 import BeautifulSoup

from source.util import LOGGER, TimeOutError, NoConnectionError, Assertor

from .settings import FINN_COMMUNITY_URL, TIMEOUT
from .finn import Finn


class FinnCommunity(Finn):
    """
    Scraper that scrapes statistics about the community in vicinity to address of Finn ad

    """

    def __init__(self, finn_code: str):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        finn_code   : str
                      Finn-code to search finn statistics for

        """
        Assertor.assert_data_types([finn_code], [str])
        super().__init__(finn_code=finn_code)

    def community_stat_response(self):
        """
        Response from Finn-no housing statistics search

        Returns
        -------
        our     : requests.models.Response
                  response with housing statistics information

        """
        try:
            try:
                start = time()
                community_stat_response = requests.get(
                    FINN_COMMUNITY_URL + "{}".format(self.finn_code),
                    timeout=TIMEOUT)
                stat_status_code = community_stat_response.status_code
                elapsed = self.elapsed_time(start)
                LOGGER.info(
                    "HTTP status code -> COMMUNITY: [{}: {}] -> elapsed: {}".format(
                        stat_status_code, responses[stat_status_code], elapsed))
                return community_stat_response
            except ConnectTimeout as finn_community_stat_timeout_error:
                raise TimeOutError(
                    "Timeout occurred - please try again later or contact system administrator, "
                    "\nexited with '{}'".format(finn_community_stat_timeout_error))
        except ConnectError as finn_community_stat_response_error:
            raise NoConnectionError(
                "Failed HTTP request - please insure that internet access is provided to the "
                "client or contact system administrator,\nexited with '{}'".format(
                    finn_community_stat_response_error))

    def community_stat_information(self):
        """
        Retrieve and parse housing ad information from Finn.no search to dict

        Returns
        -------
        out     : dict

        """
        try:
            LOGGER.info(
                "trying to retrieve '{}' for -> '{}'".format(
                    self.community_stat_information.__name__,
                    self.finn_code))
            response = self.community_stat_response()
            info = {}
            try:
                community_stat_soup = BeautifulSoup(response.content, "lxml")

                # with open('content.html', 'w', encoding='utf-8') as f:
                #     f.write(stat_soup.prettify())

                info = json.loads(
                    community_stat_soup.find("script", attrs={"id": "__NEXT_DATA__"}).contents[0])

                # with open('data.json', 'w', encoding='utf-8') as f:
                #     json.dump(info, f, ensure_ascii=False, indent=4)

                return info
            except AttributeError as no_community_statistics_exception:
                LOGGER.debug("No community statistics found!, exited with '{}'".format(
                    no_community_statistics_exception))
        except Exception as community_stat_information_exception:
            LOGGER.exception(community_stat_information_exception)
            raise community_stat_information_exception

    def to_json(self, file_dir: str = "report/json/finn_information"):
        """
        save statistics information to JSON file

        """
        Assertor.assert_data_types([file_dir], [str])
        self.save_json(self.community_stat_information(), file_dir,
                       file_prefix="CommunityStatInfo_")
        LOGGER.success(
            "'community_stat_information' successfully parsed to JSON at '{}'".format(file_dir))
