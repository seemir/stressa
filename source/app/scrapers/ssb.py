# -*- coding: utf-8 -*-

"""
Implementation of scaper against ssb market interest rates for mortgage applications

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import requests

from source.util import Assertor, LOGGER

from ..settings import SSB_URL
from .ssb_payload import SsbPayload
from .scraper import Scraper


class Ssb(Scraper):
    """
    Interest rates from SSB table nr. 10748

    """

    def __init__(self, payload: SsbPayload = None):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        payload     : SsbPayload
                      SSB compatible JSON dictionary

        """
        try:
            super().__init__()
            Assertor.assert_data_types([payload], [(type(None), SsbPayload)])
            self._payload = SsbPayload() if not payload else payload
            LOGGER.success(
                "created '{}', with id: [{}]".format(self.__class__.__name__, self.id_str))
        except Exception as ssb_exception:
            LOGGER.exception(ssb_exception)
            raise ssb_exception

    @property
    def payload(self):
        """
        Payload getter

        Returns
        -------
        out     : SsbPayload
                  active payload in object

        """
        return self._payload

    @payload.setter
    def payload(self, pay_load: SsbPayload = None):
        """
        Payload setter

        Parameters
        ----------
        pay_load      : SsbPayload
                        new payload to be set

        """
        Assertor.assert_data_types([pay_load], [(type(None), SsbPayload)])
        self._payload = pay_load

    def response(self):
        """
        submits and gets response for SSB request

        Returns
        -------
        out     : requests.models.Response
                  response with interest rate information

        """
        payload = self._payload.payload()
        response = requests.post(url=SSB_URL, json=payload)
        LOGGER.info(
            "HTTP status code -> [{}: {}]".format(response.status_code, response.reason))
        return response

    def ssb_interest_rates(self):
        """
        gets the interest information from SSB table nr. 10748

        Returns
        -------
        out     : dict
                  interest rate information from SSB

        """

        try:
            LOGGER.info("trying to retrieve '{}'".format(self.ssb_interest_rates.__name__))
            response = self.response().json()
            keys = response["dimension"]["Rentebinding"]["category"]["label"].values()
            values = response["value"]
            LOGGER.success(
                "'{}' successfully retrieved".format(self.ssb_interest_rates.__name__))
            return {key.lower(): str(val) for key, val in dict(zip(keys, values)).items()}
        except Exception as ssb_interest_rates_exception:
            LOGGER.exception(ssb_interest_rates_exception)
            raise ssb_interest_rates_exception

    def to_json(self, file_dir: str = "report/json/interest_rates"):
        """
        save ssb interest rate information to JSON

        Parameters
        ----------
        file_dir    : str
                      file directory to save JSON files

        """
        self.save_json(self.ssb_interest_rates(), file_dir=file_dir,
                       file_prefix="SsbInterestRates_")
        LOGGER.success(
            "'{}' successfully parsed to JSON at '{}'".format(self.ssb_interest_rates.__name__,
                                                              file_dir))
