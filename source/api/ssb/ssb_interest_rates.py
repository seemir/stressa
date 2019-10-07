# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.api.ssb.ssb_payload import SsbPayload
from source.util.assertor import Assertor
from source.api.api_query import ApiQuery
from source.settings import ssb_link
import requests


class SsbInterestRates(ApiQuery):
    """
    Interest rates from SSB table nr. 10748

    """

    def __init__(self, payload: SsbPayload):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        payload     : SsbPayload
                      SSB compatible JSON dictionary

        """
        Assertor.assert_date_type({payload: SsbPayload})
        super().__init__()
        self.payload = payload

    def get_response(self):
        """
        Submits and gets response for SSB request

        Returns
        -------
        out     : requests.models.Response
                  response with interest rate information

        """
        payload = self.payload.get_payload()
        return requests.post(url=ssb_link, json=payload)

    def get_interest_rates(self):
        """
        gets the interest information from SSB table nr. 10748

        Returns
        -------
        out     : dict
                  interest rate information from SSB

        """
        response = self.get_response().json()
        keys = response["dimension"]["Rentebinding"]["category"]["label"].values()
        values = response["value"]
        return dict(zip(keys, values))

    def to_json(self, file_dir: str = "report/json/interest_rates"):
        """
        save Zip code information to JSON

        Parameters
        ----------
        file_dir    : str
                      file directory to save JSON files

        """
        self._to_json(self.get_interest_rates(), file_dir=file_dir, file_title="SsbInterestRates_")
