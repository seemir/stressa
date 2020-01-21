# -*- coding: utf-8 -*-

"""
Module for the Signal abstract base class

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from abc import ABC
from uuid import uuid4

from pydot import Node


class Signal(Node, ABC):
    """
    Implementation of Signal abstract base class

    """

    def __init__(self, data, desc):
        """
        Constructor / Instantiating class

        Parameters
        ----------
        data        : object
                      data to pass in or out from operation
        desc        : str
                      description of operation

        """
        self.data = data.__dict__.keys() if not isinstance(data, dict) else data.keys()
        self.desc = desc
        super().__init__(name=str(uuid4()), style="dotted", shape="record",
                         label="keys\\<{}\\> \\n {}".format(
                             str(list(self.data)).translate({39: None}), self.desc))
