# -*- coding: utf-8 -*-

"""
Module with logic for Process superclass

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
from threading import Thread
from queue import Queue
import platform

import asyncio
from time import time
from abc import ABC, abstractmethod

from pydot import Dot, Edge

from source.util import Assertor, __version__, profiling_config, LOGGER, Debugger, Tracking

from .signal import Signal

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class Process(Dot, ABC):
    """
    Implementation of Process class, i.e. similar to a Dot graph

    """
    profiling = None
    elapsed = 0.0
    start = None

    @classmethod
    def start_process(cls):
        """
        method for starting logging and profiling of process

        """
        LOGGER.info(f"starting '{cls.__name__}'")
        cls.start = time()
        cls.profiling = profiling_config()

    @classmethod
    def end_process(cls):
        """
        method for ending logging and profiling of process

        """
        digits = 7
        elapsed = round((time() - cls.start) * 1000, digits)
        speedup = round(cls.elapsed - elapsed, digits)
        cls.profiling.add_row(["-----------", "", "", ""])
        cls.profiling.add_row(["total", "", "", f"{elapsed}ms"])
        cls.profiling.add_row(["", "", "", ""])
        cls.profiling.add_row(["speedup", "", "", f"{speedup}ms"])
        cls.profiling.add_row(
            ["(total without speedup)", "", "", f"{round(cls.elapsed, digits)}ms"])
        LOGGER.success(f"ending '{cls.__name__}'")
        LOGGER.info(f"reporting profiling results -> \n\n profiling: '{cls.__name__}' \n\n" +
                    f"{str(cls.profiling)}\n")

    def run_parallel(self, methods):
        """
        method for running multiple independent methods in parallel using multi-threading

        Parameters
        ----------
        methods     : list
                      list of methods to run in parallel

        """
        threads = []
        for method in methods:
            thread = Thread(target=method)
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

        self.threading_exception()

    def threading_exception(self):
        """
        Method for retrieving any exceptions caused by any parallel running threads

        """
        if not self.exception_queue.empty():
            raise self.exception_queue.get()

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
                         label=f"{name} - Stressa v.{__version__}")
        self._signal = {}
        self._exception_queue = Queue()

    @abstractmethod
    def input_operation(self, data: object):
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

    @property
    def exception_queue(self):
        """
        exception_queue getter

        Returns
        -------
        out         : Queue
                      active exception_queue in object

        """
        return self._exception_queue

    @Tracking
    def add_signal(self, signal: Signal, key: str):
        """
        method for adding signal to workflow

        """
        Assertor.assert_data_types([signal, key], [Signal, str])
        self.signal.update({key: signal})
        self.add_node(signal)

    @Tracking
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
        signal = self.signal.get(key, None)
        return signal

    @Tracking
    def add_transition(self, node_1, node_2, label: str = "default", thread=False):
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
        thread      : bool
                      thread boolean

        """
        color = "blue" if (label == "thread" or thread) else "gray"
        transition = Edge(node_1, node_2, color=color, label=label)
        self.add_edge(transition)

    @Debugger
    def print_pdf(self, output_format='pdf'):
        """
        method for printing a pdf with the procedure graph

        """
        file_name = "".join(
            f"-{char.lower()}" if char.isupper() else char for char in self.__class__.__name__)
        upper_dir = os.path.dirname
        procedure_dir = os.path.join(upper_dir(upper_dir(__file__)), "procedure")
        if not os.path.exists(procedure_dir):
            os.makedirs(procedure_dir)
        if output_format == 'pdf':
            self.write_pdf(os.path.join(procedure_dir, f"{file_name[1:]}.pdf"))
        elif output_format == 'png':
            self.write_png(os.path.join(procedure_dir, f"{file_name[1:]}.png"))
