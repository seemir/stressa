# -*- coding: windows-1252 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.secrets.secrets import api_link, api_form
from source.util.evaluator import Evaluator
from source.domain.family import Family
import xml.etree.ElementTree as Et
from mechanize import Browser
from bs4 import BeautifulSoup
import datetime
import json
import os


class Sifo:
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
        self.browser.open(api_link)
        self.browser.select_form(api_form)

        Evaluator.evaluate_data_type({family: Family})
        self.family = family

    def get_response(self):
        """
        Submits and get response for SIFO request

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

    def to_json(self, file_dir="expenses/json"):
        """

        Parameters
        ----------
        file_dir    : str
                      file directory to save JSON files

        """
        Evaluator.evaluate_data_type({file_dir: str})

        try:
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
        except Exception as e:
            raise OSError("creation of dir " + file_dir + " failed with: " + str(e))

        js = json.dumps(self.get_expenses(), indent=3, separators=(',', ': '), ensure_ascii=False)
        local_time = datetime.datetime.now().isoformat().replace(":", "-").replace(".", "-")
        file = open(os.path.join(file_dir, "SifoExpenditureReport_" + local_time + ".json"), "w")
        file.write(js)
        file.close()
