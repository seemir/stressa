# -*- coding: utf-8 -*-
"""
Module with the logic for the PeopleData sub-process

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Profiling, Tracking, Debugger

from .engine import Process, InputOperation, Signal, Extract, \
    Restructure, RestructurePois, Multiplex, OutputOperation


class PeopleDataProcessing(Process):
    """
    Implementation of processing of people statistics

    """

    @Tracking
    def __init__(self, people_data: dict):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        people_data      : dict
                           dict with people statistics

        """
        super().__init__(name=self.__class__.__name__)
        self.start_process()
        self.input_operation(people_data)

        self.run_parallel(
            [self.extract_1, self.extract_2, self.extract_3, self.extract_4, self.extract_5])

        self.run_parallel(
            [self.restructure_1, self.restructure_2, self.restructure_3, self.restructure_4,
             self.restructure_5])

        self.multiplex()
        self.people_statistics = self.output_operation()
        self.end_process()

    @Profiling
    @Tracking
    def input_operation(self, data: object):
        """
        initial operation of the process

        """
        Assertor.assert_data_types([data], [dict])
        input_operation = InputOperation("People Statistics")
        self.add_node(input_operation)

        input_signal = Signal(data, desc="People Statistics")
        self.add_signal(input_signal, "input_signal")
        self.add_transition(input_operation, input_signal)

    @Profiling
    @Debugger
    def extract_1(self):
        """
        method for extracting age distribution from people data

        """
        try:
            input_signal = self.get_signal("input_signal")
            age_distribution_operation = Extract(input_signal.data, "age_distribution")
            self.add_node(age_distribution_operation)
            self.add_transition(input_signal, age_distribution_operation, label="thread")
            age_distribution = age_distribution_operation.run()
            age_distribution_signal = Signal(age_distribution, "Age Distribution of Community")
            self.add_signal(age_distribution_signal, "age_distribution")
            self.add_transition(age_distribution_operation, age_distribution_signal, label="thread")
        except Exception as extract_exception:
            self.exception_queue.put(extract_exception)

    @Profiling
    @Debugger
    def extract_2(self):
        """
        method for extracting civil status distribution

        """
        try:
            input_signal = self.get_signal("input_signal")
            civil_status_operation = Extract(input_signal.data, "civil_status")
            self.add_node(civil_status_operation)
            self.add_transition(input_signal, civil_status_operation, label="thread")
            civil_status = civil_status_operation.run()
            civil_status_signal = Signal(civil_status, "Civil Status Distribution of Community")
            self.add_signal(civil_status_signal, "civil_status")
            self.add_transition(civil_status_operation, civil_status_signal, label="thread")
        except Exception as extract_exception:
            self.exception_queue.put(extract_exception)

    @Profiling
    @Debugger
    def extract_3(self):
        """
        method for extracting education distribution

        """
        try:
            input_signal = self.get_signal("input_signal")
            education_operation = Extract(input_signal.data, "education")
            self.add_node(education_operation)
            self.add_transition(input_signal, education_operation, label="thread")
            education = education_operation.run()
            education_signal = Signal(education, "Education Distribution of Community")
            self.add_signal(education_signal, "education")
            self.add_transition(education_operation, education_signal, label="thread")
        except Exception as extract_exception:
            self.exception_queue.put(extract_exception)

    @Profiling
    @Debugger
    def extract_4(self):
        """
        method for extracting income distribution

        """
        try:
            input_signal = self.get_signal("input_signal")
            income_operation = Extract(input_signal.data, "income")
            self.add_node(income_operation)
            self.add_transition(input_signal, income_operation, label="thread")
            income = income_operation.run()
            income_signal = Signal(income, "Income Distribution of Community")
            self.add_signal(income_signal, "income")
            self.add_transition(income_operation, income_signal, label="thread")
        except Exception as extract_exception:
            self.exception_queue.put(extract_exception)

    @Profiling
    @Debugger
    def extract_5(self):
        """
        method for extracting information about higher educational institutions

        """
        try:
            input_signal = self.get_signal("input_signal")
            higheducation_operation = Extract(input_signal.data, "higheducation")
            self.add_node(higheducation_operation)
            self.add_transition(input_signal, higheducation_operation, label="thread")
            higheducation = higheducation_operation.run()
            higheducation_signal = Signal(higheducation,
                                          "Information about Higher Educational Institutions")
            self.add_signal(higheducation_signal, "higheducation")
            self.add_transition(higheducation_operation, higheducation_signal, label="thread")

        except Exception as extract_exception:
            self.exception_queue.put(extract_exception)

    @Profiling
    @Debugger
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
        except Exception as restructure_exception:
            self.exception_queue.put(restructure_exception)

    @Profiling
    @Debugger
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
        except Exception as restructure_exception:
            self.exception_queue.put(restructure_exception)

    @Profiling
    @Debugger
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
        except Exception as restructure_exception:
            self.exception_queue.put(restructure_exception)

    @Profiling
    @Debugger
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
        except Exception as restructure_exception:
            self.exception_queue.put(restructure_exception)

    @Profiling
    @Debugger
    def restructure_5(self):
        """
        method for restructuring pois JSON node to pandas dataframe dict

        """
        try:
            higheducation = self.get_signal("higheducation")
            higheducation_rest_operation = RestructurePois(
                higheducation.data["higheducation"],
                "Restructure Higher Education Info to DataFrame Dict")
            self.add_node(higheducation_rest_operation)
            self.add_transition(higheducation, higheducation_rest_operation, label="thread")

            higheducation_rest = higheducation_rest_operation.run()

            higheducation_rest_signal = Signal(higheducation_rest,
                                               "Restructured Information about Higher Educational "
                                               "Institutions")
            self.add_signal(higheducation_rest_signal, "higheducation_rest")

            self.add_transition(higheducation_rest_operation, higheducation_rest_signal,
                                label="thread")
        except Exception as restructure_exception:
            self.exception_queue.put(restructure_exception)

    @Profiling
    @Debugger
    def multiplex(self):
        """
        multiplex all processed people data

        """
        age_distribution = self.get_signal("age_rest")
        civil_status_distribution = self.get_signal("civil_status_rest")
        education_distribution = self.get_signal("education_rest")
        income_distribution = self.get_signal("income_rest")
        pois_distribution = self.get_signal("higheducation_rest")

        multiplex_operation = Multiplex(
            [age_distribution.data, civil_status_distribution.data, education_distribution.data,
             income_distribution.data, pois_distribution.data],
            desc="Multiplex People Statistics")
        self.add_node(multiplex_operation)

        self.add_transition(age_distribution, multiplex_operation)
        self.add_transition(civil_status_distribution, multiplex_operation)
        self.add_transition(education_distribution, multiplex_operation)
        self.add_transition(income_distribution, multiplex_operation)
        self.add_transition(pois_distribution, multiplex_operation)

        multiplex = multiplex_operation.run()

        multiplex_signal = Signal(multiplex, "Multiplexed People Statistics")
        self.add_signal(multiplex_signal, "multiplexed_people_statistics")
        self.add_transition(multiplex_operation, multiplex_signal)

    @Profiling
    @Debugger
    def output_operation(self):
        """
        final operation of the process

        """
        multiplexed_people_statistics = self.get_signal("multiplexed_people_statistics")
        output_operation = OutputOperation("Processed Finn People Statistics")

        self.add_node(output_operation)
        self.add_transition(multiplexed_people_statistics, output_operation)
        # self.print_pdf()

        return multiplexed_people_statistics.data
