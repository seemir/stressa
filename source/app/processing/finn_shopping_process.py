# -*- coding: utf-8 -*-
"""
This module contains logic for handling the shopping statistics in a Finn Advert

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Profiling, Tracking, Debugger

from .engine import Process, InputOperation, Signal


class FinnShoppingProcess(Process):
    """
    Process for handling the shopping statistics connected to a Finn advert

    """

    @Tracking
    def __init__(self, shopping_data: dict):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        shopping_data       : dict
                              dictionary with shopping statistics

        """
        super().__init__(name=self.__class__.__name__)
        self.start_process()
        self.input_operation(shopping_data)

        self.shopping_statistics = self.output_operation()
        self.end_process()

    @Profiling
    @Tracking
    def input_operation(self, data: object):
        """
        initial operation of the process

        """
        Assertor.assert_data_types([data], [dict])
        input_operation = InputOperation("Shopping Statistics")
        self.add_node(input_operation)

        input_signal = Signal(data, desc="Shopping Statistics", prettify_keys=True, length=4)
        self.add_signal(input_signal, "input_signal")
        self.add_transition(input_operation, input_signal)

    @Profiling
    @Debugger
    def output_operation(self):
        """
        final operation of the process

        """
        self.print_pdf()
