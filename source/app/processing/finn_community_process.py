# -*- coding: utf-8 -*-
"""
Process that handles the Community Statistics from Finn

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, LOGGER, Profiling

from .engine import Process, InputOperation, Signal


class FinnCommunityProcess(Process):
    """
    Implementation of processing of community statistics

    """

    def __init__(self, community_json: dict):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        community_json      : dict
                              JSON object as dict with community statistics

        """
        try:
            self.start_process()
            super().__init__(name=self.__class__.__name__)
            self.input_operation(community_json)
            self.end_process()
        except Exception as finn_community_process_exception:
            LOGGER.exception(finn_community_process_exception)
            raise finn_community_process_exception

    @Profiling
    def input_operation(self, data: object):
        """
        initial operation of the process

        """
        Assertor.assert_data_types([data], [dict])
        input_operation = InputOperation("Community / Nabolag JSON")
        self.add_node(input_operation)

        input_signal = Signal(data, desc="Community / Nabolag JSON")
        self.add_signal(input_signal, "input_signal")

        self.add_transition(input_operation, input_signal)

    def output_operation(self):
        """
        final operation of the process

        """
