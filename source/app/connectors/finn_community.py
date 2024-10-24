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

from source.util import LOGGER, TimeOutError, NoConnectionError, Assertor, Tracking

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
                    "Timeout occurred - please try again later or contact system "
                    "administrator, exited with '{}'".format(finn_community_stat_timeout_error))
        except ConnectError as finn_community_stat_response_error:
            raise NoConnectionError(
                "Failed HTTP request - please insure that internet access is provided to the "
                "client or contact system administrator, exited with '{}'".format(
                    finn_community_stat_response_error))

    @Tracking
    def community_stat_information(self):
        """
        Retrieve and parse housing ad information from Finn.no search to dict

        Returns
        -------
        out     : dict

        """
        LOGGER.info(
            "trying to retrieve 'community_stat_information' for -> '{}'".format(self.finn_code))
        response = self.community_stat_response()
        info = {}
        try:
            community_stat_soup = BeautifulSoup(response.content, "lxml")

            # with open('content.html', 'w', encoding='utf-8') as file:
            #     file.write(community_stat_soup.prettify())

            nabolag_soup = json.loads(
                community_stat_soup.find("script", attrs={"id": "__NEXT_DATA__"}).contents[0])

            nabolag = nabolag_soup["props"]["initialState"]["nabolag"]["data"]
            if not nabolag:
                raise AttributeError("empty community data")

            info.update({"nabolag": nabolag})

            # with open('community_data.json', 'w', encoding='utf-8') as file:
            #     json.dump(info, file, ensure_ascii=False, indent=4)

            LOGGER.success("'community_stat_information' successfully retrieved")
            return info

        except AttributeError as no_community_statistics_exception:
            LOGGER.debug("[{}] No community statistics found!, exited with '{}'".format(
                self.__class__.__name__, no_community_statistics_exception))

    @Tracking
    def to_json(self, file_dir: str = "report/json/finn_information"):
        """
        save statistics information to JSON file

        """
        Assertor.assert_data_types([file_dir], [str])
        self.save_json(self.community_stat_information(), file_dir,
                       file_prefix="CommunityStatInfo_")
        LOGGER.success(
            "'community_stat_information' successfully parsed to JSON at '{}'".format(file_dir))
