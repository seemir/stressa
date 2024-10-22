# -*- coding: utf-8 -*-

"""
Implementation of connector against posten.no postal code search

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from time import time

import re
from http.client import responses
from requests.exceptions import ConnectTimeout, ConnectionError as ConnectError
import requests

from source.util import Assertor, LOGGER, InvalidData, NoConnectionError, TimeOutError, Tracking
from .settings import POSTEN_URL, TIMEOUT
from .connector import Connector


class Posten(Connector):
    """
    Posten.no postboks search connector

    """

    @Tracking
    def validate_postal_code(self):
        """
        static method for validating Norwegian postal codes

        """
        valid_postal = re.compile("[0-9]{4}").search(self.postal_code)
        if not valid_postal:
            raise InvalidData(
                "'{}' is an invalid postal code".format(self.postal_code))

    def __init__(self, postal_code: str):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        postal_code    : str
                         postal code to be searched

        """
        try:
            super().__init__()
            Assertor.assert_data_types([postal_code], [str])
            self._postal_code = postal_code
            self.validate_postal_code()
            LOGGER.success(
                "created '{}', with id: [{}]".format(self.__class__.__name__, self.id_))
        except Exception as posten_exception:
            LOGGER.exception(posten_exception)
            raise posten_exception

    @property
    def postal_code(self):
        """
        postal code getter

        Returns
        -------
        out     : str
                  active postal code attribute

        """
        return self._postal_code

    @postal_code.setter
    def postal_code(self, code):
        """
        postal code setter

        Parameters
        ----------
        code    : str
                  new postal code to be set

        """
        Assertor.assert_data_types([code], [str])
        self._postal_code = code
        self.validate_postal_code()

    @Tracking
    def response(self):
        """
        Submits and gets response for posten request

        Returns
        -------
        out         : mechanize._response.response_seek_wrapper
                      response with expenses information

        """
        try:
            try:
                start = time()
                posten_response = requests.get(POSTEN_URL + "{}".format(self.postal_code),
                                               timeout=TIMEOUT)
                posten_status_code = posten_response.status_code
                elapsed = self.elapsed_time(start)
                LOGGER.info(
                    "HTTP status code -> POSTEN: [{}: {}] -> elapsed: {}".format(
                        posten_status_code, responses[posten_status_code], elapsed))
                return posten_response
            except ConnectTimeout as posten_timeout_error:
                raise TimeOutError(
                    "Timeout occurred - please try again later or contact system "
                    "administrator, exited with '{}'".format(posten_timeout_error))
        except ConnectError as posten_response_error:
            raise NoConnectionError(
                "Failed HTTP request - please insure that internet access is provided to the "
                "client or contact system administrator, exited with '{}'".format(
                    posten_response_error))

    @Tracking
    def postal_code_info(self):
        """
        gets postal code information

        Returns
        -------
        out         : dict
                      dictionary with postal code information

        """
        LOGGER.info("trying to retrieve 'postal_code_info' for -> '{}'".format(self.postal_code))

        response = self.response().json()['postal_codes'][0]
        data = {'postnr': response['postal_code'],
                'poststed': response['city'],
                'kommune': response['primary_county'],
                'fylke': response['primary_municipality']}
        return data

    @Tracking
    def to_json(self, file_dir: str = "report/json/postal_code"):
        """
        save postal code information to JSON

        Parameters
        ----------
        file_dir    : str
                      file directory to save JSON files

        """
        self.save_json(self.postal_code_info(), file_dir=file_dir, file_prefix="PostalCode_")
        LOGGER.success("'postal_code_info' successfully parsed to JSON at '{}'".format(file_dir))

    @staticmethod
    def rules():
        """
        list of all rules in this connector

        Returns
        -------
        out         : list
                      all rules in connector
        """
        return ", ".join(["only_numeric_values", "max_len_four"]).replace("'", "")
