# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.api.ssb.ssb_payload import SsbPayload
from source.secrets.secrets import ssb_link
from source.util.evaluator import Evaluator
import datetime
import requests
import json
import os


class SsbInterestRates:
    """
    Interest rates from SSB table nr. 10748

    """

    def __init__(self, payload):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        payload     : SsbPayload
                      SSB compatible JSON dictionary

        """
        Evaluator.evaluate_data_type({payload: SsbPayload})
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

    def to_json(self, file_dir="report/json/interest_rates"):
        """
        save Zip code information to JSON

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

        js = json.dumps(self.get_interest_rates(), indent=2, separators=(',', ': '),
                        ensure_ascii=False)
        local_time = datetime.datetime.now().isoformat().replace(":", "-").replace(".", "-")
        file = open(os.path.join(file_dir, "InterestRatesInfo_" + local_time + ".json"), "w")
        file.write(js)
        file.close()
