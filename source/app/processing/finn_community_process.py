# -*- coding: utf-8 -*-
"""
Process that handles the Community Statistics from Finn

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, LOGGER, Profiling

from .engine import Process, InputOperation, Signal, Extract, Separate


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
            self.extract_1()
            self.separate()
            self.end_process()
        except Exception as finn_community_process_exception:
            LOGGER.debug("community processing not possible, exited with '{}'".format(
                finn_community_process_exception))

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
    def extract_1(self):
        """
        method for extracting community information / statistics from community JSON

        """
        input_signal = self.get_signal("input_signal")
        extract_people_operation = Extract(input_signal.data["nabolag"], "people")
        self.add_node(extract_people_operation)
        self.add_transition(input_signal, extract_people_operation)

        extract_people = extract_people_operation.run()
        extract_people_signal = Signal(extract_people, desc="Extracted People Information")
        self.add_signal(extract_people_signal, "people_signal")
        self.add_transition(extract_people_operation, extract_people_signal)

    @Profiling
    def separate(self):
        """
        method for separating list of dict to dict of dict

        """
        people_signal = self.get_signal("people_signal")
        separate_operation = Separate(people_signal.data["people"],
                                      "Separate Out People Statistics")
        self.add_node(separate_operation)
        self.add_transition(people_signal, separate_operation)

        separate = separate_operation.run()
        separate_signal = Signal(separate, "Separated People Statistics")
        self.add_signal(separate_signal, "separate_signal")
        self.add_transition(separate_operation, separate_signal)

    @Profiling
    def output_operation(self):
        """
        final operation of the process

        """
