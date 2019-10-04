# -*- coding: windows-1252 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.settings import sifo_link, sifo_form
from source.util.assertor import Assertor
from source.api.api_query import ApiQuery
from source.domain.family import Family
import xml.etree.ElementTree as Et
from mechanize import URLError
from bs4 import BeautifulSoup


class SifoExpenses(ApiQuery):
    """
    class that produces SIFO expenses given family information

    """

    def __init__(self, family):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        family      : Family
                      object with family information
        """
        Assertor.assert_date_type({family: Family})
        super().__init__()

        try:
            self.browser.open(sifo_link)
        except Exception as e:
            raise URLError("connection failed to open with '{}'".format(e))

        self.browser.select_form(sifo_form)
        self.family = family

    def get_response(self):
        """
        Submits and gets response for SIFO request

        Returns
        -------
        out         : mechanize._response.response_seek_wrapper
                      response with expenses information

        """
        for prop, value in self.family.get_properties().items():
            if prop == 'inntekt':
                self.browser[prop] = value
            else:
                self.browser[prop] = [value]
        return self.browser.submit()

    def get_expenses(self):
        """
        get SIFO expenses given the family information

        Returns
        -------
        out         : dict
                      dictionary with SIFO expenses

        """
        soup = BeautifulSoup(self.get_response(), "xml").prettify()
        root = Et.fromstring(soup)

        expenses = {}
        for child in root:
            expenses.update({child.tag: child.text.strip().replace(".", "")})
        return expenses

    def to_json(self, file_dir="report/json/expenses"):
        """
        save expenses report to JSON

        Parameters
        ----------
        file_dir    : str
                      file directory to save JSON files

        """
        self._to_json(self.get_expenses(), file_dir=file_dir, file_title="SifoExpenses_")
