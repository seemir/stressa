# -*- coding: windows-1252 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.secrets.secrets import sifo_link, sifo_form
from source.util.evaluator import Evaluator
from source.api.api_query import ApiQuery
from source.domain.family import Family
from mechanize import Browser, URLError
import xml.etree.ElementTree as Et
from bs4 import BeautifulSoup
import datetime
import json
import os


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
        self.browser = Browser()
        self.browser.set_handle_robots(False)
        self.browser.set_handle_refresh(False)

        try:
            self.browser.open(sifo_link)
        except Exception as e:
            raise URLError("connection failed to open with '{}'".format(e))

        self.browser.select_form(sifo_form)

        Evaluator.evaluate_data_type({family: Family})
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
