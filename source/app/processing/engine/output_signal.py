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

    def __init__(self, data: object, desc: str, prettify_keys: bool = False, length: int = 15):
        """
        Constructor / Instantiating class

        Parameters
        ----------
        data            : object
                          data to pass in or out from operation
        desc            : str
                          description of operation
        prettify_keys   : bool
                          True if one wants to prettify keys in data
        length          : int
                          length to apply new line, default is 15

        """
        Assertor.assert_data_types([data, desc, prettify_keys, length], [object, str, bool, int])
        super().__init__(data=data, desc=desc, prettify_keys=prettify_keys, length=length,
                         style="dashed", color="blue", penwidth=1.5)
