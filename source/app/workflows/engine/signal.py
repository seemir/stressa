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
    Implementation of the Signal abstract base class

    """

    def __init__(self, data, desc, style="dotted", **attrs):
        """
        Constructor / Instantiating class

        Parameters
        ----------
        data        : object
                      data to pass in or out from operation
        desc        : str
                      description of operation

        """
        if hasattr(data, "__dict__"):
            self.keys = data.__dict__.keys()
        elif isinstance(data, dict):
            self.keys = data.keys()
        else:
            self.keys = ""
        self.desc = desc
        self.data = data
        super().__init__(name=str(uuid4()), shape="record", style=style,
                         label="keys\\<{}\\> \\n {} \\<type '{}'\\>".format(
                             str(list(self.keys)).translate({39: None}), self.desc,
                             data.__class__.__name__), **attrs)
