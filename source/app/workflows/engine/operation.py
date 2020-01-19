# -*- coding: utf-8 -*-

"""
Module with logic for Operation class used in WorkFlow engine

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from pydot import Node


class Operation(Node):
    """
    Implementation of the Operation Node

    """

    def __init__(self, data, name, label):
        """
        Constructor / Instantiating class

        Parameters
        ----------
        data        : object
                      data the gets passed to operation
        name        : str
                      name of operation
        label       : str
                      label to display in graph, i.e. Dot compatible

        """
        super().__init__(name=name, label=label)
        self.data = data
