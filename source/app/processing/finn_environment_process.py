# -*- coding: utf-8 -*-
"""
Module containing logic for processing environment statistics

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Profiling, Tracking, Debugger

from .engine import Process, InputOperation, Signal, Extract, Restructure, RestructureRatings, \
    Multiplex, OutputOperation


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

        self.run_parallel([self.restructure_1, self.restructure_2, self.restructure_3,
                           self.restructure_4, self.restructure_5, self.restructure_6,
                           self.restructure_7, self.restructure_8, self.restructure_9,
                           self.restructure_10])

        self.multiplex()
        self.environment_statistics = self.output_operation()
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
    def restructure_1(self):
        """
        method for restructuring housing stock

        """
        housing_stock = self.get_signal("housing_stock")
        housing_stock_rest_operation = Restructure(housing_stock.data["housing_stock"],
                                                   "Restructuring Housing Stock Statistics")
        self.add_node(housing_stock_rest_operation)
        self.add_transition(housing_stock, housing_stock_rest_operation, label="thread")

        housing_stock_rest = housing_stock_rest_operation.run()

        housing_stock_rest_signal = Signal(housing_stock_rest,
                                           "Restructured Housing Stock Statistics")

        self.add_signal(housing_stock_rest_signal, "housing_stock_rest")
        self.add_transition(housing_stock_rest_operation, housing_stock_rest_signal)

    @Profiling
    @Debugger
    def restructure_2(self):
        """
        method for restructuring housing ownership

        """
        housing_ownership = self.get_signal("housing_ownership")
        housing_ownership_rest_operation = Restructure(housing_ownership.data["housing_ownership"],
                                                       "Restructuring Housing Ownership Statistics")
        self.add_node(housing_ownership_rest_operation)
        self.add_transition(housing_ownership, housing_ownership_rest_operation, label="thread")

        housing_ownership_rest = housing_ownership_rest_operation.run()

        housing_ownership_rest_signal = Signal(housing_ownership_rest,
                                               "Restructured Housing Ownership Statistics")

        self.add_signal(housing_ownership_rest_signal, "housing_ownership_rest")
        self.add_transition(housing_ownership_rest_operation, housing_ownership_rest_signal)

    @Profiling
    @Debugger
    def restructure_3(self):
        """
        method for restructuring safety rating

        """
        safety_rating = self.get_signal("safety_rating")
        if safety_rating.data:
            safety_rating_rest_operation = RestructureRatings(safety_rating.data["rating_safety"],
                                                              "Restructuring Safety Rating",
                                                              key="Trygghet")
            self.add_node(safety_rating_rest_operation)
            self.add_transition(safety_rating, safety_rating_rest_operation, label="thread")

            safety_rating_rest = {"safety_rating": safety_rating_rest_operation.run()}

            safety_rating_rest_signal = Signal(safety_rating_rest,
                                               "Restructured Safety Rating Statistics")

            self.add_signal(safety_rating_rest_signal, "safety_rating_rest")
            self.add_transition(safety_rating_rest_operation, safety_rating_rest_signal)
        else:
            safety_rating_rest = {"safety_rating": ""}
            safety_rating_rest_signal = Signal(safety_rating_rest,
                                               "Restructured Safety Rating Statistics")

            self.add_signal(safety_rating_rest_signal, "safety_rating_rest")
            self.add_transition(safety_rating, safety_rating_rest_signal)

    @Profiling
    @Debugger
    def restructure_4(self):
        """
        method for restructuring noise rating

        """
        noise_rating = self.get_signal("noise_rating")
        if noise_rating.data:
            noise_rating_rest_operation = RestructureRatings(noise_rating.data["rating_noise"],
                                                             "Restructuring Noise Rating",
                                                             key="Støynivå")
            self.add_node(noise_rating_rest_operation)
            self.add_transition(noise_rating, noise_rating_rest_operation, label="thread")

            noise_rating_rest = {"noise_rating": noise_rating_rest_operation.run()}
            noise_rating_rest_signal = Signal(noise_rating_rest,
                                              "Restructured Noise Rating Statistics")

            self.add_signal(noise_rating_rest_signal, "noise_rating_rest")
            self.add_transition(noise_rating_rest_operation, noise_rating_rest_signal)
        else:
            noise_rating_rest = {"noise_rating": ""}
            noise_rating_rest_signal = Signal(noise_rating_rest,
                                              "Restructured Noise Rating Statistics")

            self.add_signal(noise_rating_rest_signal, "noise_rating_rest")
            self.add_transition(noise_rating, noise_rating_rest_signal)

    @Profiling
    @Debugger
    def restructure_5(self):
        """
        method for restructuring environment rating

        """
        environment_rating = self.get_signal("environment_rating")
        if environment_rating.data:
            environment_rating_rest_operation = RestructureRatings(
                environment_rating.data["rating_environment"], "Restructuring Environment Rating")
            self.add_node(environment_rating_rest_operation)
            self.add_transition(environment_rating, environment_rating_rest_operation,
                                label="thread")

            environment_rating_rest = {
                "environment_rating": environment_rating_rest_operation.run()}
            environment_rating_rest_signal = Signal(environment_rating_rest,
                                                    "Restructured Environment Rating Statistics")

            self.add_signal(environment_rating_rest_signal, "environment_rating_rest")
            self.add_transition(environment_rating_rest_operation, environment_rating_rest_signal)
        else:
            environment_rating_rest = {
                "environment_rating": ""}
            environment_rating_rest_signal = Signal(environment_rating_rest,
                                                    "Restructured Environment Rating Statistics")

            self.add_signal(environment_rating_rest_signal, "environment_rating_rest")
            self.add_transition(environment_rating, environment_rating_rest_signal)

    @Profiling
    @Debugger
    def restructure_6(self):
        """
        method for restructuring garden rating

        """
        gardens_rating = self.get_signal("gardens_rating")
        if gardens_rating.data:
            garden_rating_rest_operation = RestructureRatings(
                gardens_rating.data["rating_gardens"], "Restructuring Garden Rating")
            self.add_node(garden_rating_rest_operation)
            self.add_transition(gardens_rating, garden_rating_rest_operation, label="thread")

            gardens_rating_rest = {"gardens_rating": garden_rating_rest_operation.run()}
            gardens_rating_rest_signal = Signal(gardens_rating_rest,
                                                "Restructured Garden Rating Statistics")

            self.add_signal(gardens_rating_rest_signal, "gardens_rating_rest")
            self.add_transition(garden_rating_rest_operation, gardens_rating_rest_signal)
        else:
            gardens_rating_rest = {"gardens_rating": ""}
            gardens_rating_rest_signal = Signal(gardens_rating_rest,
                                                "Restructured Garden Rating Statistics")

            self.add_signal(gardens_rating_rest_signal, "gardens_rating_rest")
            self.add_transition(gardens_rating, gardens_rating_rest_signal)

    @Profiling
    @Debugger
    def restructure_7(self):
        """
        method for restructuring roads rating

        """
        roads_rating = self.get_signal("roads_rating")
        if roads_rating.data:
            roads_rating_rest_operation = RestructureRatings(
                roads_rating.data["rating_roads"], "Restructuring Roads Rating")
            self.add_node(roads_rating_rest_operation)
            self.add_transition(roads_rating, roads_rating_rest_operation, label="thread")

            roads_rating_rest = {"roads_rating": roads_rating_rest_operation.run()}
            roads_rating_rest_signal = Signal(roads_rating_rest,
                                              "Restructured Roads Rating Statistics")

            self.add_signal(roads_rating_rest_signal, "roads_rating_rest")
            self.add_transition(roads_rating_rest_operation, roads_rating_rest_signal)
        else:
            roads_rating_rest = {"roads_rating": ""}
            roads_rating_rest_signal = Signal(roads_rating_rest,
                                              "Restructured Roads Rating Statistics")

            self.add_signal(roads_rating_rest_signal, "roads_rating_rest")
            self.add_transition(roads_rating, roads_rating_rest_signal)

    @Profiling
    @Debugger
    def restructure_8(self):
        """
        method for restructuring Housing Area

        """
        housing_area = self.get_signal("housing_area")
        housing_area_rest_operation = Restructure(
            housing_area.data["housing_area"], "Restructuring Housing Area")
        self.add_node(housing_area_rest_operation)
        self.add_transition(housing_area, housing_area_rest_operation, label="thread")

        housing_rating_rest = {"housing_area": housing_area_rest_operation.run()}
        housing_rating_rest_signal = Signal(housing_rating_rest,
                                            "Restructured Housing Area Statistics")

        self.add_signal(housing_rating_rest_signal, "housing_rating_rest")
        self.add_transition(housing_area_rest_operation, housing_rating_rest_signal)

    @Profiling
    @Debugger
    def restructure_9(self):
        """
        method for restructuring Housing Age

        """
        housing_age = self.get_signal("housing_age")
        housing_age_rest_operation = Restructure(housing_age.data["housing_age"],
                                                 "Restructuring Housing Age")
        self.add_node(housing_age_rest_operation)
        self.add_transition(housing_age, housing_age_rest_operation, label="thread")

        housing_age_rest = {"housing_age": housing_age_rest_operation.run()}
        housing_age_rest_signal = Signal(housing_age_rest, "Restructured Housing Age")

        self.add_signal(housing_age_rest_signal, "housing_age_rest")
        self.add_transition(housing_age_rest_operation, housing_age_rest_signal)

    @Profiling
    @Debugger
    def restructure_10(self):
        """
        method for restructuring Housing Prices

        """
        housing_prices = self.get_signal("housing_prices")
        if housing_prices.data:
            housing_prices_rest_operation = Restructure(housing_prices.data["housing_prices"],
                                                        "Restructuring Housing Prices")
            self.add_node(housing_prices_rest_operation)
            self.add_transition(housing_prices, housing_prices_rest_operation, label="thread")

            housing_prices_rest = {"housing_prices": housing_prices_rest_operation.run()}
            housing_prices_rest_signal = Signal(housing_prices_rest, "Restructured Housing Prices")

            self.add_signal(housing_prices_rest_signal, "housing_prices_rest")
            self.add_transition(housing_prices_rest_operation, housing_prices_rest_signal)
        else:
            housing_prices_rest = {"housing_prices": ""}
            housing_prices_rest_signal = Signal(housing_prices_rest, "Restructured Housing Prices")

            self.add_signal(housing_prices_rest_signal, "housing_prices_rest")
            self.add_transition(housing_prices, housing_prices_rest_signal)

    @Profiling
    @Debugger
    def multiplex(self):
        """
        method for multiplexing all statistics information

        """
        housing_stock_rest = self.get_signal("housing_stock_rest")
        housing_ownership_rest = self.get_signal("housing_ownership_rest")
        safety_rating_rest = self.get_signal("safety_rating_rest")
        noise_rating_rest = self.get_signal("noise_rating_rest")
        environment_rating_rest = self.get_signal("environment_rating_rest")
        gardens_rating_rest = self.get_signal("gardens_rating_rest")
        roads_rating_rest = self.get_signal("roads_rating_rest")
        housing_rating_rest = self.get_signal("housing_rating_rest")
        housing_age_rest = self.get_signal("housing_age_rest")
        housing_prices_rest = self.get_signal("housing_prices_rest")

        multiplex_operation = Multiplex([housing_stock_rest.data, housing_ownership_rest.data,
                                         safety_rating_rest.data, noise_rating_rest.data,
                                         environment_rating_rest.data, gardens_rating_rest.data,
                                         roads_rating_rest.data, housing_rating_rest.data,
                                         housing_age_rest.data, housing_prices_rest.data],
                                        desc="Multiplex Environment Statistics")

        self.add_transition(housing_stock_rest, multiplex_operation)
        self.add_transition(housing_ownership_rest, multiplex_operation)
        self.add_transition(safety_rating_rest, multiplex_operation)
        self.add_transition(noise_rating_rest, multiplex_operation)
        self.add_transition(environment_rating_rest, multiplex_operation)
        self.add_transition(gardens_rating_rest, multiplex_operation)
        self.add_transition(roads_rating_rest, multiplex_operation)
        self.add_transition(housing_rating_rest, multiplex_operation)
        self.add_transition(housing_age_rest, multiplex_operation)
        self.add_transition(housing_prices_rest, multiplex_operation)

        self.add_node(multiplex_operation)

        multiplex = multiplex_operation.run()
        multiplex_signal = Signal(multiplex, "Multiplexed Environment Statistics",
                                  prettify_keys=True, length=5)
        self.add_signal(multiplex_signal, "multiplex_environment_statistics")

        self.add_transition(multiplex_operation, multiplex_signal)

    @Profiling
    @Debugger
    def output_operation(self):
        """
        final operation of the process

        """
        multiplexed_environment_statistics = self.get_signal("multiplex_environment_statistics")
        output_operation = OutputOperation("Processed Environment Statistics")
        self.add_node(output_operation)
        self.add_transition(multiplexed_environment_statistics, output_operation)
        self.print_pdf()

        return multiplexed_environment_statistics.data
