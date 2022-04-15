# -*- coding: utf-8 -*-
"""
Module with logic for the Posten Postal code information connector

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking

from ...connectors import POSTEN_URL, Posten

from .operation import Operation


class PostalCodeInfoConnector(Operation):
    """
    Operation that retrieves Postal Code from Norwegian Postal Code Information from Postens
    public address search

    """

    @Tracking
    def __init__(self, postal_code: str):
        """
        Constructor / Instantiating class

        Parameters
        ----------
        postal_code       : str
                            postal_code for advert to retrieve information from

        """
        Assertor.assert_data_types([postal_code], [str])
        self.name = self.__class__.__name__
        super().__init__(name=self.name,
                         desc="from: '{}' \\n id: Postal Code Info Connector".format(
                             POSTEN_URL))
        self.postal_code = postal_code

    @Tracking
    def run(self):
        """
        method for running the operation

        Returns
        -------
        out         : dict
                      dictionary with postal_code information

        """
        postal_code_info = Posten(self.postal_code)
        return postal_code_info.postal_code_info()
