# -*- coding: utf-8 -*-
"""
Process that handles the Community Statistics from Finn

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Profiling, Tracking

from .engine import Process, InputOperation, Signal, Extract, Separate, \
    Restructure, RestructurePois, Multiplex, OutputOperation


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
        self.extract_2()
        self.extract_3()
        self.separate()
        self.extract_4()

        self.run_parallel(
            [self.restructure_1, self.restructure_2, self.restructure_3,
             self.restructure_4, self.restructure_5])

        self.multiplex()
        self.finn_community_statistics = self.output_operation()

        self.end_process()

    @Profiling
    @Tracking
    def input_operation(self, data: object):
        """
        initial operation of the process

        """
        Assertor.assert_data_types([data], [dict])
        input_operation = InputOperation("Finn Community Statistics")
        self.add_node(input_operation)

        input_signal = Signal(data, desc="Finn Community Statistics")
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
    def extract_2(self):
        """
        method for extracting general information

        """
        input_signal = self.get_signal("input_signal")
        extract_general_operation = Extract(input_signal.data["nabolag"], "general")
        self.add_node(extract_general_operation)
        self.add_transition(input_signal, extract_general_operation)

        extract_general = extract_general_operation.run()
        extract_general_signal = Signal(extract_general, "Extract General Information")
        self.add_signal(extract_general_signal, "general_signal")
        self.add_transition(extract_general_operation, extract_general_signal)

    @Profiling
    def extract_3(self):
        """
        method for extracting info from general information

        """
        general_signal = self.get_signal("general_signal")
        extract_info_operation = Extract(general_signal.data["general"], "info")
        self.add_node(extract_info_operation)
        self.add_transition(general_signal, extract_info_operation)

        extract_info = extract_info_operation.run()
        extract_info_signal = Signal(extract_info, "Extract Info Information")
        self.add_signal(extract_info_signal, "info_signal")
        self.add_transition(extract_info_operation, extract_info_signal)

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
    def extract_4(self):
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
        pois_signal = Signal(pois, "Information about Higher Educational Institutions")

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
    def restructure_1(self):
        """
        method for restructuring age_distribution JSON node to pandas dataframe dict

        """
        try:
            age_distribution = self.get_signal("age_distribution")
            age_distribution_rest_operation = Restructure(
                age_distribution.data["age_distribution"],
                "Restructure Age Distribution to DataFrame Dict")
            self.add_node(age_distribution_rest_operation)
            self.add_transition(age_distribution, age_distribution_rest_operation, label="thread")

            age_distribution_rest = age_distribution_rest_operation.run()

            age_distribution_rest_signal = Signal(age_distribution_rest,
                                                  "Restructured Age Distribution")
            self.add_signal(age_distribution_rest_signal, "age_rest")

            self.add_transition(age_distribution_rest_operation, age_distribution_rest_signal,
                                label="thread")
        except Exception as restructure_frame_exception:
            self.exception_queue.put(restructure_frame_exception)
            raise restructure_frame_exception

    @Profiling
    @Tracking
    def restructure_2(self):
        """
        method for restructuring civil_status JSON node to pandas dataframe dict

        """
        try:
            civil_status = self.get_signal("civil_status")
            civil_status_rest_operation = Restructure(
                civil_status.data["civil_status"],
                "Restructure Civil Status to DataFrame Dict")
            self.add_node(civil_status_rest_operation)
            self.add_transition(civil_status, civil_status_rest_operation, label="thread")

            civil_status_rest = civil_status_rest_operation.run()

            civil_status_rest_signal = Signal(civil_status_rest,
                                              "Restructured Civil Status Distribution")
            self.add_signal(civil_status_rest_signal, "civil_status_rest")

            self.add_transition(civil_status_rest_operation, civil_status_rest_signal,
                                label="thread")
        except Exception as restructure_frame_exception:
            self.exception_queue.put(restructure_frame_exception)
            raise restructure_frame_exception

    @Profiling
    @Tracking
    def restructure_3(self):
        """
        method for restructuring education JSON node to pandas dataframe dict

        """
        try:
            education = self.get_signal("education")
            education_rest_operation = Restructure(education.data["education"],
                                                   "Restructure Education to DataFrame Dict")
            self.add_node(education_rest_operation)
            self.add_transition(education, education_rest_operation, label="thread")

            education_rest = education_rest_operation.run()

            education_rest_signal = Signal(education_rest, "Restructured Education Distribution")
            self.add_signal(education_rest_signal, "education_rest")

            self.add_transition(education_rest_operation, education_rest_signal,
                                label="thread")
        except Exception as restructure_frame_exception:
            self.exception_queue.put(restructure_frame_exception)
            raise restructure_frame_exception

    @Profiling
    @Tracking
    def restructure_4(self):
        """
        method for restructuring income JSON node to pandas dataframe dict

        """
        try:
            income = self.get_signal("income")
            income_rest_operation = Restructure(income.data["income"],
                                                "Restructure Income to DataFrame Dict")
            self.add_node(income_rest_operation)
            self.add_transition(income, income_rest_operation, label="thread")

            income_rest = income_rest_operation.run()

            income_rest_signal = Signal(income_rest, "Restructured Income Distribution")
            self.add_signal(income_rest_signal, "income_rest")

            self.add_transition(income_rest_operation, income_rest_signal,
                                label="thread")
        except Exception as restructure_frame_exception:
            self.exception_queue.put(restructure_frame_exception)
            raise restructure_frame_exception

    @Profiling
    @Tracking
    def restructure_5(self):
        """
        method for restructuring pois JSON node to pandas dataframe dict

        """
        try:
            pois = self.get_signal("pois")
            pois_rest_operation = RestructurePois(pois.data["pois"],
                                                  "Restructure POIS to DataFrame Dict")
            self.add_node(pois_rest_operation)
            self.add_transition(pois, pois_rest_operation, label="thread")

            pois_rest = pois_rest_operation.run()

            pois_rest_signal = Signal(pois_rest,
                                      "Restructured Information about Higher Educational "
                                      "Institutions")
            self.add_signal(pois_rest_signal, "pois_rest")

            self.add_transition(pois_rest_operation, pois_rest_signal,
                                label="thread")
        except Exception as restructure_frame_exception:
            self.exception_queue.put(restructure_frame_exception)
            raise restructure_frame_exception

    @Profiling
    @Tracking
    def multiplex(self):
        """
        multiplex all processed data

        """
        age_distribution = self.get_signal("age_rest")
        civil_status_distribution = self.get_signal("civil_status_rest")
        education_distribution = self.get_signal("education_rest")
        income_distribution = self.get_signal("income_rest")
        pois_distribution = self.get_signal("pois_rest")
        info_signal = self.get_signal("info_signal")

        multiplex_operation = Multiplex(
            [age_distribution.data, civil_status_distribution.data, education_distribution.data,
             income_distribution.data, pois_distribution.data, info_signal.data],
            desc="Multiplex Finn Community Statistics")
        self.add_node(multiplex_operation)

        self.add_transition(age_distribution, multiplex_operation)
        self.add_transition(civil_status_distribution, multiplex_operation)
        self.add_transition(education_distribution, multiplex_operation)
        self.add_transition(income_distribution, multiplex_operation)
        self.add_transition(pois_distribution, multiplex_operation)
        self.add_transition(info_signal, multiplex_operation)

        multiplex = multiplex_operation.run()

        multiplex_signal = Signal(multiplex, "Multiplexed Finn Community Statistics")
        self.add_signal(multiplex_signal, "multiplexed_finn_community_statistics")
        self.add_transition(multiplex_operation, multiplex_signal)

    @Profiling
    @Tracking
    def output_operation(self):
        """
        final operation of the process

        """
        multiplexed_community_statistics = self.get_signal("multiplexed_finn_community_statistics")
        output_operation = OutputOperation("Finn Community Statistics")

        self.add_node(output_operation)
        self.add_transition(multiplexed_community_statistics, output_operation)
        # self.print_pdf()

        return multiplexed_community_statistics.data
