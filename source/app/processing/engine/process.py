# -*- coding: utf-8 -*-

"""
Module with logic for Process superclass

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from time import time
from abc import ABC, abstractmethod

from pydot import Dot, Edge

from source.util import Assertor, __version__, profiling_config, LOGGER

from .signal import Signal


class Process(Dot, ABC):
    """
    Implementation of Process class, i.e. similar to a Dot graph

    """
    profiling = None
    start = None

    @classmethod
    def start_process(cls):
        """
        method for starting logging and profiling of process

        """
        LOGGER.info("starting '{}'".format(cls.__name__))
        cls.start = time()
        cls.profiling = profiling_config()

    @classmethod
    def end_process(cls):
        """
        method for ending logging and profiling of process

        """
        cls.profiling.add_row(["---------", "", "", ""])
        cls.profiling.add_row(["total", "", "", str(round((time() - cls.start) * 1000, 7)) + "ms"])
        LOGGER.success("ending '{}'".format(cls.__name__))
        LOGGER.info("reporting profiling results -> \n\n profiling: '{}' \n\n".format(
            cls.__name__) + str(cls.profiling) + "\n")

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
        super().__init__(name, graph_type="digraph", labelloc="t", labeljust="left",
                         label="{} - Stressa v.{}".format(name, __version__))
        self._signal = {}

    @abstractmethod
    def input_operation(self, data):
        """
        method that captures input behaviour

        """

    @abstractmethod
    def output_operation(self):
        """
        method that captures output behaviour

        """

    @property
    def signal(self):
        """
        signal getter

        Returns
        -------
        out      : dict
                   active _signal property

        """
        return self._signal

    @signal.setter
    def signal(self, new_signal):
        """
        signal setter

        Parameters
        ----------
        new_signal  : dict
                      new signal to set in workflow

        """
        Assertor.assert_data_types([new_signal], [dict])
        self._signal = new_signal

    def add_signal(self, signal: Signal, key=str):
        """
        method for adding signal to workflow

        """
        Assertor.assert_data_types([signal, key], [Signal, str])
        self.signal.update({key: signal})
        self.add_node(signal)

    def get_signal(self, key: str):
        """
        method for retrieving a signal from WorkFlow

        Parameters
        ----------
        key     : str

        Returns
        -------
        out     :
                value in signal dictionary in WorkFlow

        """
        Assertor.assert_data_types([key], [str])
        if key in self.signal.keys():
            signal = self.signal[key]
        else:
            signal = None
        return signal

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