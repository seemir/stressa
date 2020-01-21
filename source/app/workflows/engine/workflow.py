# -*- coding: utf-8 -*-

"""
Module with logic for WorkFlow superclass

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from abc import ABC, abstractmethod

from pydot import Dot, Edge

from source.util import Assertor


class WorkFlow(Dot, ABC):
    """
    Implementation of WorkFlow class, i.e. similar to a Dot graph

    """

    @abstractmethod
    def __init__(self, name: str):
        """
        Constructor / Instantiating class

        Parameters
        ----------
        name    : str
                  name of workflow

        """
        Assertor.assert_data_types([name], [str])
        super().__init__(name, graph_type="digraph")

    def add_transition(self, node_1, node_2, label: str = "default"):
        """
        method for adding a transition between nodes in workflow

        Parameters
        ----------
        node_1      : Node
                      first node in transition
        node_2      : Node
                      second node in transition
        label       : str
                      label to be displayed

        """
        transition = Edge(node_1, node_2, color="gray", label=label)
        self.add_edge(transition)
