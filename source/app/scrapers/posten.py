# -*- coding: utf-8 -*-

"""
Implementation of scaper against posten.no postal code search

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from time import time

import re
from http.client import responses

from urllib.error import URLError
from bs4 import BeautifulSoup

from source.util import Assertor, LOGGER, NotFoundError, NoConnectionError, TimeOutError, Tracking
from .settings import POSTEN_URL, POSTEN_FORM, TIMEOUT
from .scraper import Scraper


class Posten(Scraper):
    """
    Posten.no postboks search scraper

    """

    @Tracking
    def validate_postal_code(self):
        """
        static method for validating Norwegian postal codes

        """
        valid_postal = re.compile("[0-9]{4}").search(self.postal_code)
        if not valid_postal:
            raise NotFoundError(
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
            start = time()
            self._browser.open(POSTEN_URL, timeout=TIMEOUT)
            self._browser.select_form(nr=0)
            self._browser[POSTEN_FORM] = self.postal_code
            response = self._browser.submit()
            elapsed = self.elapsed_time(start)
            LOGGER.info(
                "HTTP status code -> POSTEN: [{}: {}] -> elapsed: {}".format(
                    response.code, responses[response.code], elapsed))
            return response
        except URLError as posten_response_error:
            if str(posten_response_error) == "<urlopen error timed out>":
                raise TimeOutError(
                    "Timeout occurred - please try again later or contact "
                    "system administrator, exited with '{}'".format(posten_response_error))
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
        soup = BeautifulSoup(self.response(), "lxml")
        rows = soup.find_all('tr')
        if len(rows) == 2:
            header = [head.text.strip().lower() for head in soup.find_all('th')]
            values = [value.text.strip().upper() if i != 4 else
                      value.text.strip().upper().rsplit(' ', 1)[0] for i, value in
                      enumerate(rows[1].find_all('td'))]
            LOGGER.success("'postal_code_info' successfully retrieved")
            return {hdr: val for hdr, val in dict(zip(header, values)).items() if val}
        raise NotFoundError("'{}' is an invalid postal code".format(self.postal_code))

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
        list of all rules in this scraper

        Returns
        -------
        out         : list
                      all rules in scraper
        """
        return ", ".join(["only_numeric_values", "max_len_four"]).replace("'", "")
