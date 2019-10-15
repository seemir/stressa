# -*- coding: windows-1252 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.settings import sifo_link, sifo_form
import xml.etree.ElementTree as Et
from source.domain import Family
from source.util import Assertor
from source.log import logger
from bs4 import BeautifulSoup
from .scraper import Scraper


class Sifo(Scraper):
    """
    class that produces SIFO expenses given family information

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
            Assertor.assert_data_type({family: Family})
            self.browser.open(sifo_link)
            self.browser.select_form(sifo_form)
        except Exception as exp:
            logger.exception(exp)
            raise exp
        self.family = family
        logger.success(
            "created crawler: '{}', with id: [{}]".format(self.__class__.__name__, self.id))

    def response(self):
        """
        Submits and gets response for SIFO request

        Returns
        -------
        out         : mechanize._response.response_seek_wrapper
                      response with expenses information

        """
        for prop, value in self.family.sifo_properties().items():
            if prop == 'inntekt':
                self.browser[prop] = value
            else:
                self.browser[prop] = [value]
        return self.browser.submit()

    def sifo_expenses(self):
        """
        get SIFO expenses given the family information

        Returns
        -------
        out         : dict
                      dictionary with SIFO expenses

        """
        try:
            soup = BeautifulSoup(self.response(), "xml").prettify()
            root = Et.fromstring(soup)
            expenses = {}
            for child in root:
                expenses.update({child.tag: child.text.strip().replace(".", "")})
        except Exception as exp:
            logger.exception(Exception)
            raise exp
        return expenses

    def to_json(self, file_dir: str = "report/json/expenses"):
        """
        save expenses report to JSON

        Parameters
        ----------
        file_dir    : str
                      file directory to save JSON files

        """
        self._to_json(self.sifo_expenses(), file_dir=file_dir, file_title="SifoExpenses_")
