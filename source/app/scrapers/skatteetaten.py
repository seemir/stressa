# -*- coding: utf-8 -*-

"""
Implementation of scaper against Skatteetaten tax calculator

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import json
from http.client import responses

import requests
from requests.exceptions import ConnectTimeout, ConnectionError as ConnectError

from source.util import Assertor, LOGGER, NoConnectionError, TimeOutError, Tracking

from source.app.scrapers.settings import SKATTEETATEN_URL, TIMEOUT
from source.app.scrapers import Scraper


class Skatteetaten(Scraper):
    """
    Class that produces estimated total Taxes for a given year

    """

    def __init__(self, year: str, income: str, age: str):
        """
        Constructor / Instantiate the class

        Parameters
        ----------


        """
        try:
            super().__init__()
            Assertor.assert_data_types([year, income], [str, str])

            self.income = income
            self.year = year
            self.age = age
            self.url = SKATTEETATEN_URL + self.year

            LOGGER.success(
                "created '{}', with id: [{}]".format(self.__class__.__name__, self.id_))
        except Exception as skatteetaten_exception:
            LOGGER.exception(skatteetaten_exception)
            raise skatteetaten_exception

    @Tracking
    def payload(self):
        """
        method for generating payload str

        """
        with open('form_data/payload.json') as json_file:
            json_data = json.load(json_file)
        return json.dumps(json_data).replace("loennsinntektNaturalytelseMvBelop",
                                             self.income).replace(
            "alderIInntektsaarVerdi", self.age)

    @Tracking
    def response(self):
        """
        submits and gets response for skatteetaten request

        Returns
        -------
        out     : requests.models.Response
                  response with interest rate information

        """
        try:
            try:
                response = requests.post(url=self.url, data=self.payload(), timeout=TIMEOUT)
                status_code = response.status_code
                LOGGER.info(
                    "HTTP status code -> [{}: {}]".format(status_code, responses[status_code]))
                return response
            except ConnectTimeout as ssb_timeout_error:
                raise TimeOutError(
                    "Timeout occurred - please try again later or contact system administrator, "
                    "exited with '{}'".format(ssb_timeout_error))
        except ConnectError as ssb_response_error:
            raise NoConnectionError(
                "Failed HTTP request - please insure that internet access is provided to the "
                "client or contact system administrator, exited with '{}'".format(
                    ssb_response_error))
