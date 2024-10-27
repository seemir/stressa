# -*- coding: utf-8 -*-

"""
Implementation of connector against ssb market interest rates for mortgage applications

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from http.client import responses

import requests
from requests.exceptions import ConnectTimeout, ConnectionError as ConnectError

from source.util import Assertor, LOGGER, NoConnectionError, TimeOutError, Tracking

from .settings import SSB_URL, TIMEOUT
from .ssb_payload import SsbPayload
from .connector import Connector


class Ssb(Connector):
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
            self._browser = None
            LOGGER.success(
                f"created '{self.__class__.__name__}', with id: [{self.id_}]")
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

    @Tracking
    def response(self):
        """
        submits and gets response for SSB request

        Returns
        -------
        out     : requests.models.Response
                  response with interest rate information

        """
        try:
            try:
                response = requests.post(url=SSB_URL, json=self.payload.payload(), timeout=TIMEOUT)
                status_code = response.status_code
                LOGGER.info(
                    f"HTTP status code -> [{status_code}: {responses[status_code]}]")
                return response
            except ConnectTimeout as ssb_timeout_error:
                raise TimeOutError(
                    f"Timeout occurred - please try again later or contact system administrator, "
                    f"exited with '{ssb_timeout_error}'")
        except ConnectError as ssb_response_error:
            raise NoConnectionError(
                f"Failed HTTP request - please ensure that internet access is provided to the "
                f"client or contact system administrator, exited with '{ssb_response_error}'")

    @Tracking
    def ssb_interest_rates(self):
        """
        gets the interest information from SSB table nr. 10748

        Returns
        -------
        out     : dict
                  interest rate information from SSB

        """

        LOGGER.info("trying to retrieve 'ssb_interest_rates'")
        response = self.response().json()
        keys = response["dimension"]["Rentebinding"]["category"]["label"].values()
        values = response["value"]
        LOGGER.success("'ssb_interest_rates' successfully retrieved")
        interest_rates = {key.lower(): str(val) for key, val in dict(zip(keys, values)).items()}
        return {'markedsrente': interest_rates['inntil 3 måneder (flytende rente)']}

    @Tracking
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
        LOGGER.success(f"'ssb_interest_rates' successfully parsed to JSON at '{file_dir}'")
