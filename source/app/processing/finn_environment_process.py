# -*- coding: utf-8 -*-
"""
Module containing logic for processing environment statistics

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Profiling, Tracking, Debugger

from .engine import Process, InputOperation, Signal, Extract


class FinnEnvironmentProcess(Process):
    """
    Implementation of processing of environment statistics

    """

    def __init__(self, environment_data: dict):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        environment_data      : dict
                                dict with environment statistics

        """
        super().__init__(name=self.__class__.__name__)
        self.start_process()
        self.input_operation(environment_data)

        self.run_parallel([self.extract_1, self.extract_2, self.extract_3,
                           self.extract_4, self.extract_5, self.extract_6,
                           self.extract_7, self.extract_8, self.extract_9,
                           self.extract_10])

        self.output_operation()
        self.end_process()

    @Profiling
    @Tracking
    def input_operation(self, data: object):
        """
        initial operation of the process

        """
        Assertor.assert_data_types([data], [dict])
        input_operation = InputOperation("Environment Statistics")
        self.add_node(input_operation)

        input_signal = Signal(data, desc="Environment Statistics", prettify_keys=True, length=5)
        self.add_signal(input_signal, "input_signal")
        self.add_transition(input_operation, input_signal)

    @Profiling
    @Debugger
    def extract_1(self):
        """
        method for extracting housing stock

        """
        try:
            input_signal = self.get_signal("input_signal")
            housing_stock_operation = Extract(input_signal.data, "housing_stock")
            self.add_node(housing_stock_operation)
            self.add_transition(input_signal, housing_stock_operation, label="thread")

            housing_stock = housing_stock_operation.run()
            housing_stock_signal = Signal(housing_stock, "Distribution of Housing")
            self.add_signal(housing_stock_signal, "housing_stock")
            self.add_transition(housing_stock_operation, housing_stock_signal, label="thread")
        except Exception as extract_exception:
            self.exception_queue.put(extract_exception)

    @Profiling
    @Debugger
    def extract_2(self):
        """
        method for extracting housing ownership shares

        """
        try:
            input_signal = self.get_signal("input_signal")
            housing_ownership_operation = Extract(input_signal.data, "housing_ownership")
            self.add_node(housing_ownership_operation)
            self.add_transition(input_signal, housing_ownership_operation, label="thread")

            housing_ownership = housing_ownership_operation.run()
            housing_ownership_signal = Signal(housing_ownership,
                                              "Distribution of Housing Ownership")
            self.add_signal(housing_ownership_signal, "housing_ownership")
            self.add_transition(housing_ownership_operation, housing_ownership_signal,
                                label="thread")
        except Exception as extract_exception:
            self.exception_queue.put(extract_exception)

    @Profiling
    @Debugger
    def extract_3(self):
        """
        method for extracting safety rating

        """
        try:
            input_signal = self.get_signal("input_signal")
            safety_rating_operation = Extract(input_signal.data, "rating_safety")
            self.add_node(safety_rating_operation)
            self.add_transition(input_signal, safety_rating_operation, label="thread")

            safety_rating = safety_rating_operation.run()
            safety_rating_signal = Signal(safety_rating, "Safety Rating")
            self.add_signal(safety_rating_signal, "safety_rating")
            self.add_transition(safety_rating_operation, safety_rating_signal, label="thread")
        except Exception as extract_exception:
            self.exception_queue.put(extract_exception)

    @Profiling
    @Debugger
    def extract_4(self):
        """
        method for extracting noise rating

        """
        try:
            input_signal = self.get_signal("input_signal")
            noise_rating_operation = Extract(input_signal.data, "rating_noise")
            self.add_node(noise_rating_operation)
            self.add_transition(input_signal, noise_rating_operation, label="thread")

            noise_rating = noise_rating_operation.run()
            noise_rating_signal = Signal(noise_rating, "Noise Rating")
            self.add_signal(noise_rating_signal, "noise_rating")
            self.add_transition(noise_rating_operation, noise_rating_signal, label="thread")
        except Exception as extract_exception:
            self.exception_queue.put(extract_exception)

    @Profiling
    @Debugger
    def extract_5(self):
        """
        method for extracting environment rating

        """
        try:
            input_signal = self.get_signal("input_signal")
            environment_rating_operation = Extract(input_signal.data, "rating_environment")
            self.add_node(environment_rating_operation)
            self.add_transition(input_signal, environment_rating_operation, label="thread")

            environment_rating = environment_rating_operation.run()
            environment_rating_signal = Signal(environment_rating, "Environment Rating")
            self.add_signal(environment_rating_signal, "environment_rating")
            self.add_transition(environment_rating_operation, environment_rating_signal,
                                label="thread")
        except Exception as extract_exception:
            self.exception_queue.put(extract_exception)

    @Profiling
    @Debugger
    def extract_6(self):
        """
        method for extracting rating gardens

        """
        try:
            input_signal = self.get_signal("input_signal")
            gardens_rating_operation = Extract(input_signal.data, "rating_gardens")
            self.add_node(gardens_rating_operation)
            self.add_transition(input_signal, gardens_rating_operation, label="thread")

            gardens_rating = gardens_rating_operation.run()
            gardens_rating_signal = Signal(gardens_rating, "Gardens Rating")
            self.add_signal(gardens_rating_signal, "gardens_rating")
            self.add_transition(gardens_rating_operation, gardens_rating_signal, label="thread")
        except Exception as extract_exception:
            self.exception_queue.put(extract_exception)

    @Profiling
    @Debugger
    def extract_7(self):
        """
        method for extracting roads ratings

        """
        try:
            input_signal = self.get_signal("input_signal")
            roads_rating_operation = Extract(input_signal.data, "rating_roads")
            self.add_node(roads_rating_operation)
            self.add_transition(input_signal, roads_rating_operation, label="thread")

            roads_rating = roads_rating_operation.run()
            roads_rating_signal = Signal(roads_rating, "Roads Rating")
            self.add_signal(roads_rating_signal, "roads_rating")
            self.add_transition(roads_rating_operation, roads_rating_signal, label="thread")
        except Exception as extract_exception:
            self.exception_queue.put(extract_exception)

    @Profiling
    @Debugger
    def extract_8(self):
        """
        method for extracting housing area

        """
        try:
            input_signal = self.get_signal("input_signal")
            housing_area_operation = Extract(input_signal.data, "housing_area")
            self.add_node(housing_area_operation)
            self.add_transition(input_signal, housing_area_operation, label="thread")

            housing_area = housing_area_operation.run()
            housing_area_signal = Signal(housing_area, "Housing Area")
            self.add_signal(housing_area_signal, "housing_area")
            self.add_transition(housing_area_operation, housing_area_signal, label="thread")
        except Exception as extract_exception:
            self.exception_queue.put(extract_exception)

    @Profiling
    @Debugger
    def extract_9(self):
        """
        method for extracting housing age

        """
        try:
            input_signal = self.get_signal("input_signal")
            housing_age_operation = Extract(input_signal.data, "housing_age")
            self.add_node(housing_age_operation)
            self.add_transition(input_signal, housing_age_operation, label="thread")

            housing_age = housing_age_operation.run()
            housing_age_signal = Signal(housing_age, "Housing Age")
            self.add_signal(housing_age_signal, "housing_age")
            self.add_transition(housing_age_operation, housing_age_signal, label="thread")
        except Exception as extract_exception:
            self.exception_queue.put(extract_exception)

    @Profiling
    @Debugger
    def extract_10(self):
        """
        method for extracting housing_prices

        """
        try:
            input_signal = self.get_signal("input_signal")
            housing_prices_operation = Extract(input_signal.data, "housing_prices")
            self.add_node(housing_prices_operation)
            self.add_transition(input_signal, housing_prices_operation, label="thread")

            housing_prices = housing_prices_operation.run()
            housing_prices_signal = Signal(housing_prices, "Housing Prices")
            self.add_signal(housing_prices_signal, "housing_prices")
            self.add_transition(housing_prices_operation, housing_prices_signal, label="thread")
        except Exception as extract_exception:
            self.exception_queue.put(extract_exception)

    @Profiling
    @Debugger
    def output_operation(self):
        """
        final operation of the process

        """
        self.print_pdf()
