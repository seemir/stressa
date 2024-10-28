# -*- coding: utf-8 -*-
"""
Module containing logic for connector against "nabolag" profiles of Finn ad

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from time import time

import json
from http.client import responses

from requests.exceptions import ConnectTimeout, ConnectionError as ConnectError
import requests

from bs4 import BeautifulSoup

from source.util import LOGGER, TimeOutError, NoConnectionError, Assertor, \
    Tracking

from .settings import FINN_COMMUNITY_URL, TIMEOUT
from .finn import Finn


class FinnCommunity(Finn):
    """
    Connector that retrieves statistics about the community in vicinity to address of Finn ad

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

    @Tracking
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
                    f"{FINN_COMMUNITY_URL}{self.finn_code}",
                    timeout=TIMEOUT)
                stat_status_code = community_stat_response.status_code
                elapsed = self.elapsed_time(start)
                LOGGER.info(
                    f"HTTP status code -> COMMUNITY: [{stat_status_code}: "
                    f"{responses[stat_status_code]}] -> elapsed: {elapsed}")
                return community_stat_response
            except ConnectTimeout as finn_community_stat_timeout_error:
                raise TimeOutError(
                    f"Timeout occurred - please try again later or contact system "
                    f"administrator, exited with '{finn_community_stat_timeout_error}'")
        except ConnectError as finn_community_stat_response_error:
            raise NoConnectionError(
                f"Failed HTTP request - please ensure that internet access is provided to the "
                f"client or contact system administrator, exited with "
                f"'{finn_community_stat_response_error}'")

    @Tracking
    def community_stat_information(self):
        """
        Retrieve and parse housing ad information from Finn.no search to dict

        Returns
        -------
        out     : dict

        """
        LOGGER.info(
            f"trying to retrieve 'community_stat_information' for -> '{self.finn_code}'")
        response = self.community_stat_response()
        info = {}
        try:
            community_stat_soup = BeautifulSoup(response.content, "lxml")

            nabolag_soup = json.loads(
                community_stat_soup.find("script", attrs={
                    "id": "__NEXT_DATA__"}).contents[0])

            nabolag = nabolag_soup["props"]["initialState"]["nabolag"]["data"]
            if not nabolag:
                raise AttributeError("empty community data")

            info.update({"nabolag": nabolag})

            LOGGER.success(
                "'community_stat_information' successfully retrieved")
            return info

        except AttributeError as no_community_statistics_exception:
            LOGGER.debug(
                f"[{self.__class__.__name__}] No community statistics found!, "
                f"exited with '{no_community_statistics_exception}'")
            return info

    @Tracking
    def to_json(self, file_dir: str = "report/json/finn_information"):
        """
        save statistics information to JSON file

        """
        Assertor.assert_data_types([file_dir], [str])
        self.save_json(self.community_stat_information(), file_dir,
                       file_prefix="CommunityStatInfo_")
        LOGGER.success(
            f"'community_stat_information' successfully parsed to JSON at '{file_dir}'")
