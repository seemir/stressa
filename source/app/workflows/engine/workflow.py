# -*- coding: utf-8 -*-

"""
Module with logic for WorkFlow superclass

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from pydot import Dot


class WorkFlow(Dot):
    """
    Implementation of WorkFlow class, i.e. similar to a Dot graph

    """

    def __init__(self, name):
        """
        Constructor / Instantiating class

        Parameters
        ----------
        name    : str
                  name of workflow

        """
        super().__init__(name, graph_type="digraph")
