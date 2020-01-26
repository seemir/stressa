# -*- coding: utf-8 -*-

"""
Module with logic of output signal

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor

from .signal import Signal


class OutputSignal(Signal):
    """
    A output signal is a signal that is outputted from a workflow

    """

    def __init__(self, data: object, desc: str):
        """
        Constructor / Instantiating class

        Parameters
        ----------
        data        : object
                      data to pass in or out from operation
        desc        : str
                      description of operation
        """
        Assertor.assert_data_types([data, desc], [object, str])
        super().__init__(data=data, desc=desc, style="dashed", color="blue", penwidth=1.5)
