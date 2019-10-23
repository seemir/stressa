# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.settings import posten_url, posten_form
from source.exception import DomainError
from source.log import main_logger
from source.util import Assertor
from bs4 import BeautifulSoup
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
            Assertor.assert_data_type({zip_code: str})
            self.browser.open(posten_url)
            self.browser.select_form(nr=0)
        except Exception as exp:
            main_logger.exception(exp)
            raise exp
        self._zip_code = zip_code
        main_logger.success(
            "created scraper: '{}', with id: [{}]".format(self.__class__.__name__, self.id))

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
        Assertor.assert_data_type({code: str})
        self._zip_code = code

    def response(self):
        """
        Submits and gets response for posten request

        Returns
        -------
        out         : mechanize._response.response_seek_wrapper
                      response with expenses information

        """
        self.browser[posten_form] = self.zip_code
        return self.browser.submit()

    def zip_code_info(self):
        """
        gets Zip code information

        Returns
        -------
        out         : dict
                      dictionary with Zip code informtion

        """
        try:
            soup = BeautifulSoup(self.response(), "lxml")
            rows = soup.find_all('tr')
            if len(rows) == 2:
                header = [head.text.strip().lower() for head in soup.find_all('th')]
                values = [value.text.strip().lower() for value in rows[1].find_all('td')]
            else:
                raise DomainError("str '{}' is an invalid ZIP code".format(self.zip_code))
        except Exception as exp:
            main_logger.exception(exp)
            raise exp
        return {hdr: val for hdr, val in dict(zip(header, values)).items() if val}

    def to_json(self, file_dir: str = "report/json/zip_code"):
        """
        save Zip code information to JSON

        Parameters
        ----------
        file_dir    : str
                      file directory to save JSON files

        """
        self._to_json(self.zip_code_info(), file_dir=file_dir, file_title="ZipCode_")
