# -*- coding: utf-8 -*-
"""
This module contains logic for handling the shopping statistics in a Finn Advert

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Profiling, Tracking, Debugger

from .engine import Process, InputOperation, Signal, Extract, RestructurePois, RestructureRatings, \
    Multiplex, OutputOperation


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

        self.run_parallel([self.extract_1, self.extract_2, self.extract_3])

        self.run_parallel([self.restructure_1, self.restructure_2, self.restructure_3])
        self.multiplex()

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
    def extract_1(self):
        """
        extract groceries information

        """
        input_signal = self.get_signal("input_signal")
        groceries_operation = Extract(input_signal.data, "groceries")
        self.add_node(groceries_operation)
        self.add_transition(input_signal, groceries_operation, label="thread")

        groceries = groceries_operation.run()
        groceries_signal = Signal(groceries, "Groceries Information")

        self.add_signal(groceries_signal, "groceries")
        self.add_transition(groceries_operation, groceries_signal, label="thread")

    @Profiling
    @Debugger
    def extract_2(self):
        """
        extract food selection information

        """
        input_signal = self.get_signal("input_signal")
        food_selection_operation = Extract(input_signal.data, "food_selection")
        self.add_node(food_selection_operation)
        self.add_transition(input_signal, food_selection_operation, label="thread")

        food_selection = food_selection_operation.run()

        food_selection_signal = Signal(food_selection, "Food Selection Rating")

        self.add_signal(food_selection_signal, "rating_food_selection")
        self.add_transition(food_selection_operation, food_selection_signal, label="thread")

    @Profiling
    @Debugger
    def extract_3(self):
        """
        extract services information

        """
        input_signal = self.get_signal("input_signal")
        services_operation = Extract(input_signal.data, "services")
        self.add_node(services_operation)
        self.add_transition(input_signal, services_operation, label="thread")

        services = services_operation.run()
        services_signal = Signal(services, "Services Information")

        self.add_signal(services_signal, "services")
        self.add_transition(services_operation, services_signal, label="thread")

    @Profiling
    @Debugger
    def restructure_1(self):
        """
        restructure groceries statistics

        """
        groceries = self.get_signal("groceries")
        groceries_rest_operation = RestructurePois(groceries.data["groceries"],
                                                   "Restructure List of Groceries Stores")
        self.add_node(groceries_rest_operation)
        self.add_transition(groceries, groceries_rest_operation, label="thread")

        groceries_rest = groceries_rest_operation.run(col_name="Butikk")
        groceries_rest_signal = Signal(groceries_rest, "Restructured List of Groceries Stores")

        self.add_signal(groceries_rest_signal, "groceries_rest")
        self.add_transition(groceries_rest_operation, groceries_rest_signal, label="thread")

    @Profiling
    @Debugger
    def restructure_2(self):
        """
        restructure rating of food selection

        """
        rating_food_selection = self.get_signal("rating_food_selection")
        if rating_food_selection.data:
            rating_food_selection_operation = RestructureRatings(
                rating_food_selection.data["food_selection"], "Restructuring Food Selection Rating",
                key="Matutvalg")
            self.add_node(rating_food_selection_operation)
            self.add_transition(rating_food_selection, rating_food_selection_operation,
                                label="thread")

            rating_food_selection_rest = {
                "rating_food_selection": rating_food_selection_operation.run()}
            rating_food_selection_rest_signal = Signal(rating_food_selection_rest,
                                                       "Restructured Food Selection Rating")

            self.add_signal(rating_food_selection_rest_signal, "rating_food_selection_rest")
            self.add_transition(rating_food_selection_operation,
                                rating_food_selection_rest_signal, label="thread")
        else:
            rating_food_selection_rest = {"rating_food_selection": ""}
            rating_food_selection_rest_signal = Signal(rating_food_selection_rest,
                                                       "Restructured Food Selection Rating")

            self.add_signal(rating_food_selection_rest_signal, "rating_food_selection_rest")
            self.add_transition(rating_food_selection, rating_food_selection_rest_signal,
                                label="thread")

    @Profiling
    @Debugger
    def restructure_3(self):
        """
        restructure service statistics

        """
        services = self.get_signal("services")
        services_rest_operation = RestructurePois(services.data["services"],
                                                  "Restructure List of Services")
        self.add_node(services_rest_operation)
        self.add_transition(services, services_rest_operation, label="thread")

        services_rest = services_rest_operation.run(col_name="Butikk")
        services_rest_signal = Signal(services_rest, "Restructured List of Services")

        self.add_signal(services_rest_signal, "services_rest")
        self.add_transition(services_rest_operation, services_rest_signal, label="thread")

    @Profiling
    @Debugger
    def multiplex(self):
        """
        method for multiplexing all shopping statistics

        """
        groceries_rest = self.get_signal("groceries_rest")
        rating_food_selection_rest = self.get_signal("rating_food_selection_rest")
        services_rest = self.get_signal("services_rest")

        multiplex_operation = Multiplex([groceries_rest.data, rating_food_selection_rest.data,
                                         services_rest.data], desc="Multiplex Shopping Statistics")

        self.add_transition(groceries_rest, multiplex_operation)
        self.add_transition(rating_food_selection_rest, multiplex_operation)
        self.add_transition(services_rest, multiplex_operation)

        self.add_node(multiplex_operation)

        multiplex = multiplex_operation.run()
        multiplex_signal = Signal(multiplex, "Multiplexed Shopping Statistics",
                                  prettify_keys=True, length=5)
        self.add_signal(multiplex_signal, "multiplex_shopping_statistics")

        self.add_transition(multiplex_operation, multiplex_signal)

    @Profiling
    @Debugger
    def output_operation(self):
        """
        final operation of the process

        """
        multiplexed_shopping_statistics = self.get_signal("multiplex_shopping_statistics")
        output_operation = OutputOperation("Processed Shopping Statistics")
        self.add_node(output_operation)
        self.add_transition(multiplexed_shopping_statistics, output_operation)
        self.print_pdf()
        return multiplexed_shopping_statistics.data
