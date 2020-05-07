# -*- coding: utf-8 -*-
"""
Process that handles the Community Statistics from Finn

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, LOGGER, Profiling

from .engine import Process, InputOperation, Signal, Extract


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
            self.extract()
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

    @Profiling
    def extract(self):
        """
        method for extracting community information / statistics from community JSON

        """
        input_signal = self.get_signal("input_signal")
        extract_people_operation = Extract(input_signal.data["nabolag"], "people")
        self.add_node(extract_people_operation)
        self.add_transition(input_signal, extract_people_operation)

        extract_people = extract_people_operation.run()
        extract_people_signal = Signal(extract_people, desc="Extract People Information")
        self.add_signal(extract_people_signal, "people_signal")
        self.add_transition(extract_people_operation, extract_people_signal)

    @Profiling
    def output_operation(self):
        """
        final operation of the process

        """
