# -*- coding: utf-8 -*-

"""
Implementation of connector against sifo budget calculator

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from time import time
from http.client import responses
from urllib.error import URLError
import requests

from source.util import Assertor, LOGGER, NoConnectionError, TimeOutError, Tracking
from source.domain import Family

from .settings import SIFO_URL, TIMEOUT
from .connector import Connector


class Sifo(Connector):
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
            self._family = family
            LOGGER.success(
                f"created '{self.__class__.__name__}', with id: [{self.id_}]")
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

    @Tracking
    def response(self):
        """
        Submits and gets response for SIFO request

        Returns
        -------
        out         : requests.Response
                      response with expenses information

        """
        try:
            start = time()
            parsed_sifo_url = SIFO_URL

            for key, item in self.family.sifo_properties().items():
                parsed_sifo_url = f"{parsed_sifo_url}{key}={item}&"

            response = requests.post(url=parsed_sifo_url, timeout=TIMEOUT)
            status_code = response.status_code

            elapsed = self.elapsed_time(start)
            LOGGER.info(
                f"HTTP status code -> SIFO: [{status_code}: {responses[status_code]}] "
                f"-> elapsed: {elapsed}")
            return response
        except URLError as sifo_response_error:
            if str(sifo_response_error) == "<urlopen error timed out>":
                raise TimeOutError(
                    f"Timeout occurred - please try again later or contact system "
                    f"administrator, exited with '{sifo_response_error}'")
            raise NoConnectionError(
                f"Failed HTTP request - please ensure that internet access is provided to the "
                f"client or contact system administrator, exited with '{sifo_response_error}'")

    @Tracking
    def sifo_base_expenses(self, include_id: bool = False):
        """
        get SIFO base expenses given the family information

        Returns
        -------
        out         : dict
                      dictionary with SIFO expenses

        """
        LOGGER.info(f"trying to retrieve '{self.sifo_base_expenses.__name__}'")

        response_json = self.response().json()["utgifter"]

        sifo_expenses = {}
        sifo_expenses.update(response_json['individspesifikke'])
        sifo_expenses.update({'sumindivid': response_json['sumindivid']})
        sifo_expenses.update(response_json['husholdsspesifikke'])
        sifo_expenses.update({'sumhusholdning': response_json['sumhusholdning']})
        sifo_expenses.update({'totalt': response_json['totalt']})
        sifo_expenses = {key: str(val) for key, val in sifo_expenses.items()}

        if include_id:
            sifo_expenses.update({'_id': self.family.id_})

        LOGGER.success(f"'{self.sifo_base_expenses.__name__}' successfully retrieved")
        return sifo_expenses

    @Tracking
    def to_json(self, file_dir: str):
        """
        save sifo expenses to JSON

        Parameters
        ----------
        file_dir    : str
                      file directory to save JSON files

        """
        self.save_json(self.sifo_base_expenses(), file_dir=file_dir, file_prefix="SifoExpenses_")
        LOGGER.success(f"'sifo_expenses' successfully parsed to JSON at '{file_dir}'")
