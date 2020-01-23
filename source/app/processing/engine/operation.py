# -*- coding: utf-8 -*-

"""
Module with logic for Operation class used in WorkFlow engine

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from uuid import uuid4
from abc import ABC, abstractmethod

from pydot import Node

from source.util import Assertor


class Operation(Node, ABC):
    """
    Implementation of the Operation Node

    """

    @abstractmethod
    def __init__(self, name: str, desc: str):
        """
        Constructor / Instantiating class

        Parameters
        ----------
        name        : str
                      name of operation
        desc        : str
                      description of operation

        """
        Assertor.assert_data_types([name, desc], [str, str])
        self.name = name
        self.desc = desc
        super().__init__(name=str(uuid4()), style="filled", fillcolor="gray", shape="record",
                         label="\\<{}\\> \\n {}".format(self.name, self.desc))

    @abstractmethod
    def run(self):
        """
        abstract method for running an operation

        """
