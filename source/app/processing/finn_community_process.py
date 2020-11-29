# -*- coding: utf-8 -*-
"""
Process that handles the Community Statistics from Finn

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Profiling, Tracking, Debugger

from .engine import Process, InputOperation, Signal, Extract, Separate, Multiplex, \
    OutputOperation

from .finn_transportation_sub_model import FinnTransportationSubModel
from .finn_environment_sub_model import FinnEnvironmentSubModel
from .finn_leisure_sub_model import FinnLeisureSubModel
from .finn_people_sub_model import FinnPeopleSubModel
from .finn_family_sub_model import FinnFamilySubModel


class FinnCommunityProcess(Process):
    """
    Implementation of processing of community statistics

    """

    @Tracking
    def __init__(self, community_json: dict):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        community_json      : dict
                              JSON object as dict with community statistics

        """
        self.start_process()
        super().__init__(name=self.__class__.__name__)
        Assertor.assert_data_types([community_json], [dict])

        self.community_json = community_json

        self.input_operation(self.community_json)

        self.run_parallel([self.extract_1, self.extract_2, self.extract_3, self.extract_4,
                           self.extract_5, self.extract_6, self.extract_7])
        self.run_parallel([self.separate_1, self.separate_2, self.extract_8, self.separate_3,
                           self.separate_4, self.separate_5, self.separate_6])

        self.run_parallel([self.people_data_processing, self.family_data_processing,
                           self.environmental_data_processing, self.transportation_data_processing,
                           self.leisure_data_processing])

        self.multiplex()

        self.finn_community_statistics = self.output_operation()
        self.end_process()

    @Profiling
    @Tracking
    def input_operation(self, data: object):
        """
        initial operation of the process

        """
        input_operation = InputOperation("Finn Community Statistics")
        self.add_node(input_operation)

        input_signal = Signal(data, desc="Finn Community Statistics")
        self.add_signal(input_signal, "input_signal")

        self.add_transition(input_operation, input_signal)

    @Profiling
    @Debugger
    def extract_1(self):
        """
        method for extracting community information / statistics from community JSON

        """
        input_signal = self.get_signal("input_signal")
        extract_people_operation = Extract(input_signal.data["nabolag"], "people")
        self.add_node(extract_people_operation)
        self.add_transition(input_signal, extract_people_operation, label="thread")

        extract_people = extract_people_operation.run()
        extract_people_signal = Signal(extract_people, desc="Extracted People Information")
        self.add_signal(extract_people_signal, "people_signal")
        self.add_transition(extract_people_operation, extract_people_signal, label="thread")

    @Profiling
    @Debugger
    def extract_2(self):
        """
        method for extracting general information

        """
        input_signal = self.get_signal("input_signal")
        extract_general_operation = Extract(input_signal.data["nabolag"], "general")
        self.add_node(extract_general_operation)
        self.add_transition(input_signal, extract_general_operation, label="thread")

        extract_general = extract_general_operation.run()
        extract_general_signal = Signal(extract_general, "Extract General Information")
        self.add_signal(extract_general_signal, "general_signal")
        self.add_transition(extract_general_operation, extract_general_signal, label="thread")

    @Profiling
    @Debugger
    def extract_3(self):
        """
        method for extracting family information

        """
        input_signal = self.get_signal("input_signal")
        extract_family_operation = Extract(input_signal.data["nabolag"], "family")
        self.add_node(extract_family_operation)
        self.add_transition(input_signal, extract_family_operation, label="thread")

        extract_family = extract_family_operation.run()
        extract_family_signal = Signal(extract_family, "Extract Family Information")
        self.add_signal(extract_family_signal, "family_signal")
        self.add_transition(extract_family_operation, extract_family_signal, label="thread")

    @Profiling
    @Debugger
    def extract_4(self):
        """
        method for extracting environment information

        """
        input_signal = self.get_signal("input_signal")
        extract_environment_operation = Extract(input_signal.data["nabolag"], "environment")
        self.add_node(extract_environment_operation)
        self.add_transition(input_signal, extract_environment_operation, label="thread")

        extract_environment = extract_environment_operation.run()
        extract_environment_signal = Signal(extract_environment, "Extract Environment Information")
        self.add_signal(extract_environment_signal, "environment_signal")
        self.add_transition(extract_environment_operation, extract_environment_signal,
                            label="thread")

    @Profiling
    @Debugger
    def extract_5(self):
        """
        method for extracting transportation info

        """
        input_signal = self.get_signal("input_signal")
        extract_transportation_operation = Extract(input_signal.data["nabolag"], "transport")
        self.add_node(extract_transportation_operation)
        self.add_transition(input_signal, extract_transportation_operation, label="thread")

        extract_transportation = extract_transportation_operation.run()
        extract_transportation_signal = Signal(extract_transportation,
                                               "Extract Transportation Information")
        self.add_signal(extract_transportation_signal, "transportation_signal")
        self.add_transition(extract_transportation_operation, extract_transportation_signal,
                            label="thread")

    @Profiling
    @Debugger
    def extract_6(self):
        """
        method for extracting leisure information

        """
        input_signal = self.get_signal("input_signal")
        extract_leisure_operation = Extract(input_signal.data["nabolag"], "leisure")
        self.add_node(extract_leisure_operation)
        self.add_transition(input_signal, extract_leisure_operation, label="thread")

        extract_leisure = extract_leisure_operation.run()
        extract_leisure_signal = Signal(extract_leisure, "Extract Leisure Information")
        self.add_signal(extract_leisure_signal, "leisure_signal")
        self.add_transition(extract_leisure_operation, extract_leisure_signal, label="thread")

    @Profiling
    @Debugger
    def extract_7(self):
        """
        method for extracting shopping information

        """
        input_signal = self.get_signal("input_signal")
        extract_shopping_operation = Extract(input_signal.data["nabolag"], "shopping")
        self.add_node(extract_shopping_operation)
        self.add_transition(input_signal, extract_shopping_operation, label="thread")

        extract_shopping = extract_shopping_operation.run()
        extract_shopping_signal = Signal(extract_shopping, "Extract Shopping Information")
        self.add_signal(extract_shopping_signal, "shopping_signal")
        self.add_transition(extract_shopping_operation, extract_shopping_signal, label="thread")

    @Profiling
    @Debugger
    def extract_8(self):
        """
        method for extracting info from general information

        """
        general_signal = self.get_signal("general_signal")
        extract_info_operation = Extract(general_signal.data["general"], "info")
        self.add_node(extract_info_operation)
        self.add_transition(general_signal, extract_info_operation, label="thread")

        extract_info = extract_info_operation.run()
        extract_info_signal = Signal(extract_info, "Extract Community Specific Information")
        self.add_signal(extract_info_signal, "info_signal")
        self.add_transition(extract_info_operation, extract_info_signal, label="thread")

    @Profiling
    @Debugger
    def separate_1(self):
        """
        method for separating list of dict with people information to dict of dict

        """
        people_signal = self.get_signal("people_signal")
        separate_operation = Separate(people_signal.data["people"],
                                      "Separate Out People Statistics")
        self.add_node(separate_operation)
        self.add_transition(people_signal, separate_operation, label="thread")

        separate = separate_operation.run()
        separate_signal = Signal(separate, "Separated People Statistics")
        self.add_signal(separate_signal, "separate_people_signal")
        self.add_transition(separate_operation, separate_signal, label="thread")

    @Profiling
    @Debugger
    def separate_2(self):
        """
        method for separating list of dict with family information to dict of dict

        """
        people_signal = self.get_signal("family_signal")
        separate_operation = Separate(people_signal.data["family"],
                                      "Separate Out Family Statistics")
        self.add_node(separate_operation)
        self.add_transition(people_signal, separate_operation, label="thread")

        separate = separate_operation.run()
        separate_signal = Signal(separate, "Separated Family Statistics", prettify_keys=True,
                                 length=5)
        self.add_signal(separate_signal, "separate_family_signal")
        self.add_transition(separate_operation, separate_signal, label="thread")

    @Profiling
    @Debugger
    def separate_3(self):
        """
        method for separating list of dict with environment information to dict of dict

        """
        environment_signal = self.get_signal("environment_signal")
        separate_operation = Separate(environment_signal.data["environment"],
                                      "Separate Out Environment Statistics")
        self.add_node(separate_operation)
        self.add_transition(environment_signal, separate_operation, label="thread")

        separate = separate_operation.run()

        separate_signal = Signal(separate, "Separated Environment Statistics", prettify_keys=True,
                                 length=5)
        self.add_signal(separate_signal, "separated_environment_signal")
        self.add_transition(separate_operation, separate_signal, label="thread")

    @Profiling
    @Debugger
    def separate_4(self):
        """
        method for separating list of dict with transportation information to dict of dict

        """
        transportation_signal = self.get_signal("transportation_signal")
        separate_operation = Separate(transportation_signal.data["transport"],
                                      "Separate Out Transportation Statistics")
        self.add_node(separate_operation)
        self.add_transition(transportation_signal, separate_operation, label="thread")

        separate = separate_operation.run()

        separate_signal = Signal(separate, "Separated Transportation Statistics",
                                 prettify_keys=True,
                                 length=4)
        self.add_signal(separate_signal, "separated_transportation_signal")
        self.add_transition(separate_operation, separate_signal, label="thread")

    @Profiling
    @Debugger
    def separate_5(self):
        """
        method for separating list of dict with leisure information to dict of dict

        """
        leisure_signal = self.get_signal("leisure_signal")
        separate_operation = Separate(leisure_signal.data["leisure"],
                                      "Separate Out Leisure Statistics")
        self.add_node(separate_operation)
        self.add_transition(leisure_signal, separate_operation, label="thread")

        separate = separate_operation.run()

        separate_signal = Signal(separate, "Separated Leisure Statistics", prettify_keys=True,
                                 length=5)
        self.add_signal(separate_signal, "separated_leisure_signal")
        self.add_transition(separate_operation, separate_signal, label="thread")

    @Profiling
    @Debugger
    def separate_6(self):
        """
        method for separating list of dict with shopping information to dict of dict

        """
        shopping_signal = self.get_signal("shopping_signal")
        separate_operation = Separate(shopping_signal.data["shopping"],
                                      "Separate Out Shopping Statistics")
        self.add_node(separate_operation)
        self.add_transition(shopping_signal, separate_operation, label="thread")

        separate = separate_operation.run()

        separate_signal = Signal(separate, "Separated Shopping Statistics", prettify_keys=True,
                                 length=5)
        self.add_signal(separate_signal, "separated_shopping_signal")
        self.add_transition(separate_operation, separate_signal, label="thread")

    @Profiling
    @Tracking
    def people_data_processing(self):
        """
        sub model for processing finn people data

        """
        people_signal = self.get_signal("separate_people_signal")
        people_processing_operation = FinnPeopleSubModel(people_signal.data)

        self.add_node(people_processing_operation)
        self.add_transition(people_signal, people_processing_operation, label="thread")

        people_processing = people_processing_operation.run()
        people_processing_signal = Signal(people_processing, "Processed People Statistics")
        self.add_signal(people_processing_signal, "people_statistics_signal")
        self.add_transition(people_processing_operation, people_processing_signal, label="thread")

    @Profiling
    @Tracking
    def family_data_processing(self):
        """
        sub model for processing finn family data

        """
        family_signal = self.get_signal("separate_family_signal")
        family_processing_operation = FinnFamilySubModel(family_signal.data)

        self.add_node(family_processing_operation)
        self.add_transition(family_signal, family_processing_operation, label="thread")

        family_processing = family_processing_operation.run()
        family_processing_signal = Signal(family_processing, "Processed Family Statistics",
                                          prettify_keys=True, length=4)
        self.add_signal(family_processing_signal, "family_statistics_signal")
        self.add_transition(family_processing_operation, family_processing_signal, label="thread")

    @Profiling
    @Debugger
    def environmental_data_processing(self):
        """
        sub model for processing finn environmental data

        """
        environmental_signal = self.get_signal("separated_environment_signal")
        environmental_processing_operation = FinnEnvironmentSubModel(environmental_signal.data)

        self.add_node(environmental_processing_operation)
        self.add_transition(environmental_signal, environmental_processing_operation,
                            label="thread")

        environmental_processing = environmental_processing_operation.run()
        environmental_processing_signal = Signal(environmental_processing,
                                                 "Processed Environmental Statistics",
                                                 prettify_keys=True, length=5)
        self.add_signal(environmental_processing_signal, "environmental_statistics_signal")
        self.add_transition(environmental_processing_operation, environmental_processing_signal,
                            label="thread")

    @Profiling
    @Debugger
    def transportation_data_processing(self):
        """
        sub model for processing finn transportation data

        """
        transportation_signal = self.get_signal("separated_transportation_signal")
        transportation_signal_operation = FinnTransportationSubModel(transportation_signal.data)

        self.add_node(transportation_signal_operation)
        self.add_transition(transportation_signal, transportation_signal_operation, label="thread")

        transportation_processing = transportation_signal_operation.run()
        transportation_processing_signal = Signal(transportation_processing,
                                                  "Processed Transportation Statistics",
                                                  prettify_keys=True, length=5)
        self.add_signal(transportation_processing_signal, "transportation_statistics_signal")
        self.add_transition(transportation_signal_operation, transportation_processing_signal,
                            label="thread")

    @Profiling
    @Debugger
    def leisure_data_processing(self):
        """
        sub model for processing finn leisure data

        """
        leisure_signal = self.get_signal("separated_leisure_signal")
        leisure_signal_operation = FinnLeisureSubModel(leisure_signal.data)

        self.add_node(leisure_signal_operation)
        self.add_transition(leisure_signal, leisure_signal_operation, label="thread")

        leisure_processing = leisure_signal_operation.run()
        leisure_processing_signal = Signal(leisure_processing, "Processed Leisure Statistics",
                                           prettify_keys=True, length=5)
        self.add_signal(leisure_processing_signal, "leisure_statistics_signal")
        self.add_transition(leisure_signal_operation, leisure_processing_signal, label="thread")

    @Profiling
    @Debugger
    def multiplex(self):
        """
        multiplex all processed data

        """
        info_signal = self.get_signal("info_signal")

        people_statistics = self.get_signal("people_statistics_signal")
        family_statistics = self.get_signal("family_statistics_signal")
        environmental_statistics = self.get_signal("environmental_statistics_signal")
        transportation_statistics = self.get_signal("transportation_statistics_signal")
        leisure_statistics = self.get_signal("leisure_statistics_signal")

        multiplex_operation = Multiplex(
            [info_signal.data, people_statistics.data, family_statistics.data,
             environmental_statistics.data, transportation_statistics.data,
             leisure_statistics.data],
            desc="Multiplex Finn Community Statistics")
        self.add_node(multiplex_operation)

        self.add_transition(info_signal, multiplex_operation)
        self.add_transition(people_statistics, multiplex_operation)
        self.add_transition(family_statistics, multiplex_operation)
        self.add_transition(environmental_statistics, multiplex_operation)
        self.add_transition(transportation_statistics, multiplex_operation)
        self.add_transition(leisure_statistics, multiplex_operation)

        multiplex = multiplex_operation.run()

        multiplex_signal = Signal(multiplex, "Multiplexed Finn Community Statistics",
                                  prettify_keys=True, length=7)
        self.add_signal(multiplex_signal, "multiplexed_finn_community_statistics")
        self.add_transition(multiplex_operation, multiplex_signal)

    @Profiling
    @Debugger
    def output_operation(self):
        """
        final operation of the process

        """
        multiplexed_community_statistics = self.get_signal("multiplexed_finn_community_statistics")
        output_operation = OutputOperation("Processed Finn Community Statistics")

        self.add_node(output_operation)
        self.add_transition(multiplexed_community_statistics, output_operation)
        self.print_pdf()

        return multiplexed_community_statistics.data
