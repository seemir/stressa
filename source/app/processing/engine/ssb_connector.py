# -*- coding: utf-8 -*-
"""
Module with logic for the Ssb market interest rates

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Tracking

from ...connectors import SSB_URL, Ssb

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

    @Tracking
    def run(self):
        """
        method for running the operation

        Returns
        -------
        out         : dict
                      dictionary with interest rates information

        """
        ssb_interest_rate = Ssb()
        return ssb_interest_rate.ssb_interest_rates()
