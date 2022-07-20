# -*- coding: utf-8 -*-
"""
Module with logic for the Ssb market interest rates

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

import json

from source.util import Tracking

from ...connectors import SSB_URL, Ssb, SsbPayload

from .operation import Operation


class SsbConnector(Operation):
    """
    Operation that retrieves market interest from ssb

    """

    @Tracking
    def __init__(self):
        """
        Constructor / Instantiating class

        """
        self.name = self.__class__.__name__
        super().__init__(name=self.name,
                         desc="from: '{}' \\n id: Market Interest Rate Connector".format(
                             SSB_URL))
        self.cache_dir = os.path.dirname(__file__) + "\\tmp\\"

    @Tracking
    def run(self):
        """
        method for running the operation

        Returns
        -------
        out         : dict
                      dictionary with interest rates information

        """

        if os.path.exists(self.cache_dir):
            with open(self.cache_dir + 'ssb_cache.json', 'r') as read_json_file:
                cached_request = json.load(read_json_file)
                read_json_file.close()

            if cached_request:
                time_of_last_request = cached_request["tid"]
            else:
                time_of_last_request = ""
        else:
            os.makedirs(self.cache_dir)
            time_of_last_request = ""

        time_of_curr_request = SsbPayload.updated_table_date()

        if time_of_curr_request != time_of_last_request:
            ssb_interest_rate = Ssb()
            market_rate = ssb_interest_rate.ssb_interest_rates()
            cached_results = {"tid": time_of_curr_request}
            cached_results.update(market_rate)

            with open(self.cache_dir + 'ssb_cache.json', 'w') as write_json_file:
                json.dump(cached_results, write_json_file)
                write_json_file.close()
        else:
            market_rate = {"markedsrente": cached_request["markedsrente"]}

        return market_rate
