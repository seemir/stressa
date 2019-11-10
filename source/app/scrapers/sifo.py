# -*- coding: windows-1252 -*-

"""
Implementation of scaper against sifo budget calculator

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import xml.etree.ElementTree as Et
from http.client import responses

from bs4 import BeautifulSoup

from source.domain import Family
from source.util import Assertor, LOGGER

from ..settings import SIFO_URL, SIFO_FORM
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
        try:
            super().__init__()
            Assertor.assert_data_types([family], [Family])
            self._browser.open(SIFO_URL)
            self._family = family
            LOGGER.success(
                "created '{}', with id: [{}]".format(self.__class__.__name__, self.id_str))
        except Exception as sifo_exception:
            LOGGER.exception(sifo_exception)
            raise sifo_exception

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
        self._browser.select_form(SIFO_FORM)
        for prop, value in self.family.sifo_properties().items():
            if prop == 'inntekt':
                self._browser[prop] = value
            else:
                self._browser[prop] = [value]
        response = self._browser.submit()
        LOGGER.info(
            "HTTP status code -> [{}: {}]".format(response.code, responses[response.code]))
        return response

    def sifo_expenses(self, include_id: bool = False):
        """
        get SIFO expenses given the family information

        Returns
        -------
        out         : dict
                      dictionary with SIFO expenses

        """

        try:
            LOGGER.info("trying to retrieve '{}'".format(self.sifo_expenses.__name__))
            soup = BeautifulSoup(self.response(), "xml")
            root = Et.fromstring(soup.prettify())
            expenses = {}
            if include_id:
                expenses.update({'_id': self.family.id_str})
            for child in root:
                expenses.update({child.tag: child.text.strip().replace(".", "")})
            LOGGER.success("'{}' successfully retrieved".format(self.sifo_expenses.__name__))
            return expenses
        except Exception as sifo_expenses_exception:
            LOGGER.exception(sifo_expenses_exception)
            raise sifo_expenses_exception

    def to_json(self, file_dir: str):
        """
        save sifo expenses to JSON

        Parameters
        ----------
        file_dir    : str
                      file directory to save JSON files

        """
        self.save_json(self.sifo_expenses(), file_dir=file_dir, file_prefix="SifoExpenses_")
        LOGGER.success(
            "'{}' successfully parsed to JSON at '{}'".format(self.sifo_expenses.__name__,
                                                              file_dir))
