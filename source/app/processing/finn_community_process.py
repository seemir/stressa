# -*- coding: utf-8 -*-
"""
Process that handles the Community Statistics from Finn

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Profiling, Tracking

from .engine import Process, InputOperation, Signal, Extract, Separate


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
        self.input_operation(community_json)
        self.extract_1()
        self.separate()
        self.extract_2()
        self.output_operation()
        self.end_process()

    @Profiling
    @Tracking
    def input_operation(self, data: object):
        """
        initial operation of the process

        """
        Assertor.assert_data_types([data], [dict])
        input_operation = InputOperation("Finn Community / Nabolag JSON")
        self.add_node(input_operation)

        input_signal = Signal(data, desc="Finn Community / Nabolag JSON")
        self.add_signal(input_signal, "input_signal")

        self.add_transition(input_operation, input_signal)

    @Profiling
    @Tracking
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
    @Tracking
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
    @Tracking
    def extract_2(self):
        """
        method for extracting community statistics from community Information

        """
        separate_signal = self.get_signal("separate_signal")
        age_distribution_operation = Extract(separate_signal.data, "age_distribution")
        civil_status_operation = Extract(separate_signal.data, "civil_status")
        education_operation = Extract(separate_signal.data, "education")
        income_operation = Extract(separate_signal.data, "income")
        pois_operation = Extract(separate_signal.data, "pois")

        self.add_node(age_distribution_operation)
        self.add_node(civil_status_operation)
        self.add_node(education_operation)
        self.add_node(income_operation)
        self.add_node(pois_operation)

        self.add_transition(separate_signal, age_distribution_operation)
        self.add_transition(separate_signal, civil_status_operation)
        self.add_transition(separate_signal, education_operation)
        self.add_transition(separate_signal, income_operation)
        self.add_transition(separate_signal, pois_operation)

        age_distribution = age_distribution_operation.run()
        civil_status = civil_status_operation.run()
        education = education_operation.run()
        income = income_operation.run()
        pois = pois_operation.run()

        age_distribution_signal = Signal(age_distribution, "Age Distribution of Community")
        civil_status_signal = Signal(civil_status, "Civil Status Distribution of Community")
        education_signal = Signal(education, "Educational Distribution of Community")
        income_signal = Signal(income, "Income Distribution of Community")
        pois_signal = Signal(pois, "List of Higher Educational Institutions")

        self.add_signal(age_distribution_signal, "age_distribution")
        self.add_signal(civil_status_signal, "civil_status")
        self.add_signal(education_signal, "education")
        self.add_signal(income_signal, "income")
        self.add_signal(pois_signal, "pois")

        self.add_transition(age_distribution_operation, age_distribution_signal)
        self.add_transition(civil_status_operation, civil_status_signal)
        self.add_transition(education_operation, education_signal)
        self.add_transition(income_operation, income_signal)
        self.add_transition(pois_operation, pois_signal)

    @Profiling
    @Tracking
    def output_operation(self):
        """
        final operation of the process

        """
        self.print_pdf()
