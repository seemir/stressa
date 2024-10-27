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
    def __init__(self, name: str, desc: str, label: str = None):
        """
        Constructor / Instantiating class

        Parameters
        ----------
        name        : str
                      name of operation
        desc        : str
                      description of operation

        """
        self.name = name
        Assertor.assert_data_types([name, desc], [str, str])
        self.desc = desc
        self.label = f"\\<{self.name}\\> \\n {self.desc}" if not label else label
        super().__init__(name=str(uuid4()), style="filled", fillcolor="gray", shape="record",
                         label=self.label)

    @abstractmethod
    def run(self):
        """
        abstract method for running an operation

        """
