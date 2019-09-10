# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.exception.invalid_zip_code import InvalidZipCode
from source.secrets.secrets import posten_link, posten_form
from source.util.evaluator import Evaluator
from source.api.api_query import ApiQuery
from mechanize import Browser, URLError
from bs4 import BeautifulSoup


class ZipCodeFinder(ApiQuery):
    """
    Zip code finder using Posten.no postboks search

    """

    def __init__(self, zip_code):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        zip_code    : str
                      Zip code to be searched

        """
        self.browser = Browser()
        self.browser.set_handle_robots(False)
        self.browser.set_handle_refresh(False)

        Evaluator.evaluate_data_type({zip_code: str})
        self.zip_code = zip_code

        try:
            self.browser.open(posten_link)
        except Exception as e:
            raise URLError("connection failed to open with '{}'".format(e))

        self.browser.select_form(nr=0)

    def get_response(self):
        """
        Submits and gets response for posten request

        Returns
        -------
        out         : mechanize._response.response_seek_wrapper
                      response with expenses information

        """
        self.browser[posten_form] = self.zip_code
        return self.browser.submit()

    def get_zip_code_info(self):
        """
        gets Zip code information

        Returns
        -------
        out         : dict
                      dictionary with Zip code informtion

        """
        soup = BeautifulSoup(self.get_response(), "html.parser")
        rows = soup.find_all('tr')
        header = [head.text.strip() for head in soup.find_all('th')]

        try:
            values = [value.text.strip() for value in rows[1].find_all('td')]
        except Exception:
            raise InvalidZipCode("ZIP code not found!")

        return dict(zip(header, values))

    def to_json(self, file_dir="report/json/zip_code"):
        """
        save Zip code information to JSON

        Parameters
        ----------
        file_dir    : str
                      file directory to save JSON files

        """
        self._to_json(self.get_zip_code_info(), file_dir=file_dir, file_title="ZipCode_")
