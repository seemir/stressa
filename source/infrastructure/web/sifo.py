# -*- coding: windows-1252 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.settings import sifo_url, sifo_form
import xml.etree.ElementTree as Et
from http.client import responses
from source.domain import Family
from source.util import Assertor
from bs4 import BeautifulSoup
from source.log import logger
from .scraper import Scraper


class Sifo(Scraper):
    """
    Class that produces SIFO expenses given family information

    """

    def __init__(self, family: Family):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        family      : Family
                      object with family information
        """
        super().__init__()
        try:
            Assertor.assert_data_types([family], [Family])
            self.browser.open(sifo_url)
            self._family = family
            logger.success(
                "created '{}', with id: [{}]".format(self.__class__.__name__, self.id))
        except Exception as exp:
            logger.exception(exp)
            raise exp

    @property
    def family(self):
        """
        family getter

        Returns
        -------
        out     : Family
                  active family object instantiated

        """
        return self._family

    @family.setter
    def family(self, fam: Family):
        """
        family setter

        """
        Assertor.assert_data_types([fam], [Family])
        self._family = fam

    def response(self):
        """
        Submits and gets response for SIFO request

        Returns
        -------
        out         : mechanize._response.response_seek_wrapper
                      response with expenses information

        """
        self.browser.select_form(sifo_form)
        for prop, value in self.family.sifo_properties().items():
            if prop == 'inntekt':
                self.browser[prop] = value
            else:
                self.browser[prop] = [value]
        response = self.browser.submit()
        logger.info(
            "HTTP status code -> [{}: {}]".format(response.code, responses[response.code]))
        return response

    def sifo_expenses(self):
        """
        get SIFO expenses given the family information

        Returns
        -------
        out         : dict
                      dictionary with SIFO expenses

        """

        try:
            logger.info("trying to retrieve '{}'".format(self.sifo_expenses.__name__))
            soup = BeautifulSoup(self.response(), "xml")
            root = Et.fromstring(soup.prettify())
            expenses = {'_id': self.family.id}
            for child in root:
                expenses.update({child.tag: child.text.strip().replace(".", "")})
            logger.success("'{}' successfully retrieved".format(self.sifo_expenses.__name__))
            return expenses
        except Exception as exp:
            logger.exception(Exception)
            raise exp

    def to_json(self, file_dir: str = "report/json/expenses"):
        """
        save sifo expenses to JSON

        Parameters
        ----------
        file_dir    : str
                      file directory to save JSON files

        """
        self._to_json(self.sifo_expenses(), file_dir=file_dir, file_title="SifoExpenses_")
        logger.success(
            "'{}' successfully parsed to JSON at '{}'".format(self.sifo_expenses.__name__,
                                                              file_dir))
