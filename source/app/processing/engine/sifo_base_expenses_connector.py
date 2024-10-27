# -*- coding: utf-8 -*-

"""
Module for operation of SIFO base expenses connector

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.domain import Family
from source.util import Assertor, Tracking

from ...connectors import SIFO_URL, Sifo

from .operation import Operation


class SifoBaseExpensesConnector(Operation):
    """
    Implementation of operation

    """

    @Tracking
    def __init__(self, data: Family):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        data     : Family
                   Sifo compatible Family object with all necessary family information

        """
        self.name = self.__class__.__name__
        Assertor.assert_data_types([data], [Family])
        super().__init__(name=self.name,
                         desc=f"from: '{SIFO_URL}' \\n id: SIFO Base Expenses Connector")
        self.data = data

    @Tracking
    def run(self):
        """
        method for running operation

        Returns
        -------
        out     : dict
                  SIFO compatible dictionary with all necessary family information

        """
        sifo = Sifo(self.data)
        return sifo.sifo_base_expenses()
