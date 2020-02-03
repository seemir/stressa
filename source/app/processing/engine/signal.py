# -*- coding: utf-8 -*-

"""
Module for the Signal abstract base class

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from abc import ABC
from uuid import uuid4

from pydot import Node

from source.util import Assertor


class Signal(Node, ABC):
    """
    Implementation of the Signal abstract base class

    """

    @staticmethod
    def remove_quotation(strings: list):
        """
        method for removing quotation marks in list of strings

        """
        return str(list(strings)).translate({39: None})

    def __init__(self, data: object, desc: str, style: str = "dotted", prettify_keys: bool = False,
                 **attrs):
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

        """
        Assertor.assert_data_types([data, desc, style, prettify_keys], [object, str, str, bool])
        if hasattr(data, "__dict__"):
            keys = data.__dict__.keys()
            self.keys = self.prettify_dict_keys(keys) if prettify_keys else self.remove_quotation(
                list(keys))
        elif isinstance(data, dict):
            keys = data.keys()
            self.keys = self.prettify_dict_keys(keys) if prettify_keys else self.remove_quotation(
                list(keys))
        else:
            self.keys = ""
        self.desc = desc
        self.data = data
        super().__init__(name=str(uuid4()), shape="record", style=style,
                         label="keys\\<{}\\> \\n {} \\<type '{}'\\>".format(
                             self.keys, self.desc, data.__class__.__name__), **attrs)

    def prettify_dict_keys(self, dict_keys):
        """
        method for prettify the dictionary keys

        Parameters
        ----------
        dict_keys   :
                      keys to prettify

        Returns
        -------
        out         : str
                      str with dictionary

        """
        pretty_keys = []
        for i, keys in enumerate(list(dict_keys)):
            if i % 15 == 0 and i != 0:
                pretty_keys.append("\n" + str(keys))
            else:
                pretty_keys.append(keys)
        return self.remove_quotation(pretty_keys)
