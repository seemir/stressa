# -*- coding: utf-8 -*-
"""
Module with logic for process that handles the leisure statistics related to a Finn Advert

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Profiling, Tracking, Debugger

from .engine import Process, InputOperation, Signal, OutputOperation


class FinnLeisureProcessing(Process):
    """
    Process for handling leisure data from Finn advert

    """

    @Tracking
    def __init__(self, leisure_data: dict):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        leisure_data  : dict
                        dictionary with leisure statistics

        """
        super().__init__(name=self.__class__.__name__)
        self.start_process()
        self.input_operation(leisure_data)

        self.leisure_statistics = self.output_operation()

        self.end_process()

    @Profiling
    @Tracking
    def input_operation(self, data: object):
        """
        initial operation of the process

        """
        Assertor.assert_data_types([data], [dict])
        input_operation = InputOperation("Leisure Statistics")
        self.add_node(input_operation)

        input_signal = Signal(data, desc="Leisure Statistics",
                              prettify_keys=True, length=4)
        self.add_signal(input_signal, "input_signal")
        self.add_transition(input_operation, input_signal)

    @Profiling
    @Debugger
    def output_operation(self):
        """
        final operation of the process

        """
        output_operation = OutputOperation("Processed Leisure Statistics")
        self.add_node(output_operation)
        self.print_pdf()
