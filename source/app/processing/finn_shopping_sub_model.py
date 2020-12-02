# -*- coding: utf-8 -*-
"""
Module with logic for sub-model for Shopping Statistics in relation to an advert

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking, Debugger

from .finn_shopping_process import FinnShoppingProcess
from .engine import SubModel


class FinnShoppingSubModel(SubModel):
    """
    Sub model that handles the shopping statistics from a Finn advert

    """

    @Tracking
    def __init__(self, shopping_data: dict):
        """
        Constructor / Instantiating the class

        Parameters
        ----------
        shopping_data       : dict
                              dictionary with shopping statistics

        """
        Assertor.assert_data_types([shopping_data], [dict])
        self.name = FinnShoppingProcess.__name__
        super().__init__(name=self.name, desc="Processing Finn Shopping Statistics")
        self.shopping_data = shopping_data

    @Debugger
    def run(self):
        """
        method for running the sub model

        """
        finn_shopping_process = FinnShoppingProcess(self.shopping_data)
        return finn_shopping_process.shopping_statistics
