# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.infrastructure.payload import SsbPayload
from source.settings import ssb_link
from source.util import Assertor
from source.log import logger
from .crawler import Crawler
import requests


class Ssb(Crawler):
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
            Assertor.assert_data_type({payload: (type(None), SsbPayload)})
            super().__init__()
            self.payload = SsbPayload() if not payload else payload
            logger.success(
                "created crawler: '{}', with id: [{}]".format(self.__class__.__name__, self.id))
        except Exception as exp:
            logger.exception(exp)
            raise exp

    def response(self):
        """
        Submits and gets response for SSB request

        Returns
        -------
        out     : requests.models.Response
                  response with interest rate information

        """
        payload = self.payload.payload()
        return requests.post(url=ssb_link, json=payload)

    def ssb_interest_rates(self):
        """
        gets the interest information from SSB table nr. 10748

        Returns
        -------
        out     : dict
                  interest rate information from SSB

        """
        try:
            response = self.response().json()
            keys = response["dimension"]["Rentebinding"]["category"]["label"].values()
            values = response["value"]
        except Exception as exp:
            logger.exception(exp)
            raise exp
        return {key.lower(): str(val) for key, val in dict(zip(keys, values)).items()}

    def to_json(self, file_dir: str = "report/json/interest_rates"):
        """
        save Zip code information to JSON

        Parameters
        ----------
        file_dir    : str
                      file directory to save JSON files

        """
        self._to_json(self.ssb_interest_rates(), file_dir=file_dir, file_title="SsbInterestRates_")
