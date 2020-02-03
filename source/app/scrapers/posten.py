# -*- coding: utf-8 -*-

"""
Implementation of scaper against posten.no zip code search

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import re
from http.client import responses

from urllib.error import URLError
from bs4 import BeautifulSoup

from source.util import Assertor, LOGGER, NotFoundError, NoConnectionError, TimeOutError
from .settings import POSTEN_URL, POSTEN_FORM, TIMEOUT
from .scraper import Scraper


class Posten(Scraper):
    """
    Posten.no postboks search scraper

    """

    @staticmethod
    def validate_zip_code(zip_code: str):
        """
        static method for validating Norwegian zip codes

        Parameters
        ----------
        zip_code

        Returns
        -------

        """
        valid_zip = re.compile("[0-9]{4}").search(zip_code)
        if not valid_zip:
            raise NotFoundError("'{}' is an invalid zip code".format(zip_code))

    def __init__(self, zip_code: str):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        zip_code    : str
                      Zip code to be searched

        """
        try:
            super().__init__()
            Assertor.assert_data_types([zip_code], [str])
            self.validate_zip_code(zip_code)
            self._zip_code = zip_code
            LOGGER.success(
                "created '{}', with id: [{}]".format(self.__class__.__name__, self.id_))
        except Exception as posten_exception:
            LOGGER.exception(posten_exception)
            raise posten_exception

    @property
    def zip_code(self):
        """
        ZIP code getter

        Returns
        -------
        out     : str
                  active ZIP code attribute

        """
        return self._zip_code

    @zip_code.setter
    def zip_code(self, code):
        """
        ZIP code setter

        Parameters
        ----------
        code    : str
                  Zip code to be searched

        """
        Assertor.assert_data_types([code], [str])
        self.validate_zip_code(code)
        self._zip_code = code

    def response(self):
        """
        Submits and gets response for posten request

        Returns
        -------
        out         : mechanize._response.response_seek_wrapper
                      response with expenses information

        """
        try:
            self._browser.open(POSTEN_URL, timeout=TIMEOUT)
            self._browser.select_form(nr=0)
            self._browser[POSTEN_FORM] = self.zip_code
            response = self._browser.submit()
            LOGGER.info(
                "HTTP status code -> [{}: {}]".format(response.code, responses[response.code]))
            return response
        except URLError as posten_response_error:
            if str(posten_response_error) == "<urlopen error timed out>":
                raise TimeOutError(
                    "Timeout occurred - please try again later or contact system administrator, "
                    "\nexited with '{}'".format(posten_response_error))
            raise NoConnectionError(
                "Failed HTTP request - please insure that internet access is provided to the "
                "client or contact system administrator,\nexited with '{}'".format(
                    posten_response_error))

    def zip_code_info(self):
        """
        gets Zip code information

        Returns
        -------
        out         : dict
                      dictionary with Zip code informtion

        """
        try:
            LOGGER.info("trying to retrieve '{}' for -> '{}'".format(self.zip_code_info.__name__,
                                                                     self.zip_code))
            soup = BeautifulSoup(self.response(), "lxml")
            rows = soup.find_all('tr')
            if len(rows) == 2:
                header = [head.text.strip().lower() for head in soup.find_all('th')]
                values = [value.text.strip().upper() if i != 4 else
                          value.text.strip().upper().rsplit(' ', 1)[0] for i, value in
                          enumerate(rows[1].find_all('td'))]
                LOGGER.success("'{}' successfully retrieved".format(self.zip_code_info.__name__))
                return {hdr: val for hdr, val in dict(zip(header, values)).items() if val}
            raise NotFoundError("'{}' is an invalid zip code".format(self.zip_code))
        except Exception as zip_code_exception:
            LOGGER.exception(zip_code_exception)
            raise zip_code_exception

    def to_json(self, file_dir: str = "report/json/zip_code"):
        """
        save Zip code information to JSON

        Parameters
        ----------
        file_dir    : str
                      file directory to save JSON files

        """
        self.save_json(self.zip_code_info(), file_dir=file_dir, file_prefix="ZipCode_")
        LOGGER.success("'zip_code_info' successfully parsed to JSON at '{}'".format(file_dir))
