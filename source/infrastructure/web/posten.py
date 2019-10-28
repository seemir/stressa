# -*- coding: utf-8 -*-

"""
Implementation of scaper against posten.no zip code search

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from bs4 import BeautifulSoup
from source.settings import POSTEN_URL, POSTEN_FORM
from source.exception import DomainError
from source.util import Assertor
from source.log import LOGGER
from .scraper import Scraper


class Posten(Scraper):
    """
    Posten.no postboks search scraper

    """

    def __init__(self, zip_code: str):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        zip_code    : str
                      Zip code to be searched

        """
        super().__init__()
        try:
            Assertor.assert_data_types([zip_code], [str])
            self._browser.open(POSTEN_URL)
            self._zip_code = zip_code
            LOGGER.success(
                "created '{}', with id: [{}]".format(self.__class__.__name__, self.id_str))
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
        self._zip_code = code

    def response(self):
        """
        Submits and gets response for posten request

        Returns
        -------
        out         : mechanize._response.response_seek_wrapper
                      response with expenses information

        """
        self._browser.select_form(nr=0)
        self._browser[POSTEN_FORM] = self.zip_code
        response = self._browser.submit()
        LOGGER.info(
            "HTTP status code -> [{}]".format(response.info().values()[12].replace(" ", ": ")))
        return response

    def zip_code_info(self):
        """
        gets Zip code information

        Returns
        -------
        out         : dict
                      dictionary with Zip code informtion

        """
        try:
            LOGGER.info("trying to retrieve '{}'".format(self.zip_code_info.__name__))
            soup = BeautifulSoup(self.response(), "lxml")
            rows = soup.find_all('tr')
            if len(rows) == 2:
                header = [head.text.strip().lower() for head in soup.find_all('th')]
                values = [value.text.strip().lower() for value in rows[1].find_all('td')]
            else:
                raise DomainError("str '{}' is an invalid ZIP code".format(self.zip_code))
            LOGGER.success("'{}' successfully retrieved".format(self.zip_code_info.__name__))
            return {hdr: val for hdr, val in dict(zip(header, values)).items() if val}
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
        self._to_json(self.zip_code_info(), file_dir=file_dir, file_prefix="ZipCode_")
        LOGGER.success(
            "'{}' successfully parsed to JSON at '{}'".format(self.zip_code_info.__name__,
                                                              file_dir))
