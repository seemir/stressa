# -*- coding: utf-8 -*-
"""
Module with logic for process that handles the leisure statistics related to a Finn Advert

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Profiling, Tracking, Debugger

from .engine import Process, InputOperation, Signal, OutputOperation, Extract, RestructurePois, \
    RestructureRatings, Multiplex


class FinnLeisureProcessing(Process):
    """
    Process for handling leisure data from Finn advert

    """

    @Tracking
    def __init__(self, leisure_data: dict):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        leisure_data  : dict
                        dictionary with leisure statistics

        """
        super().__init__(name=self.__class__.__name__)
        self.start_process()
        self.input_operation(leisure_data)

        self.run_parallel([self.extract_1, self.extract_2, self.extract_3, self.extract_4])

        self.run_parallel([self.restructure_1, self.restructure_2, self.restructure_3,
                           self.restructure_4])

        self.multiplex()

        self.leisure_statistics = self.output_operation()

        self.end_process()

    @Profiling
    @Tracking
    def input_operation(self, data: object):
        """
        initial operation of the process

        """
        Assertor.assert_data_types([data], [dict])
        input_operation = InputOperation("Leisure Statistics")
        self.add_node(input_operation)

        input_signal = Signal(data, desc="Leisure Statistics", prettify_keys=True, length=4)
        self.add_signal(input_signal, "input_signal")
        self.add_transition(input_operation, input_signal)

    @Profiling
    @Debugger
    def extract_1(self):
        """
        extract sports information

        """
        input_signal = self.get_signal("input_signal")
        sport_operation = Extract(input_signal.data, "sport")
        self.add_node(sport_operation)
        self.add_transition(input_signal, sport_operation, label="thread")

        sport = sport_operation.run()
        sport_signal = Signal(sport, "Sport Information")

        self.add_signal(sport_signal, "sport")
        self.add_transition(sport_operation, sport_signal, label="thread")

    @Profiling
    @Debugger
    def extract_2(self):
        """
        extract rating of activity

        """
        input_signal = self.get_signal("input_signal")
        rating_activity_operation = Extract(input_signal.data, "rating_activity")
        self.add_node(rating_activity_operation)
        self.add_transition(input_signal, rating_activity_operation, label="thread")

        rating_activity = rating_activity_operation.run()
        rating_activity_signal = Signal(rating_activity, "Activity Rating")

        self.add_signal(rating_activity_signal, "rating_activity")
        self.add_transition(rating_activity_operation, rating_activity_signal, label="thread")

    @Profiling
    @Debugger
    def extract_3(self):
        """
        extract rating of serving

        """
        input_signal = self.get_signal("input_signal")
        rating_serving_operation = Extract(input_signal.data, "rating_serving")
        self.add_node(rating_serving_operation)
        self.add_transition(input_signal, rating_serving_operation, label="thread")

        rating_serving = rating_serving_operation.run()
        rating_serving_signal = Signal(rating_serving, "Serving Rating")

        self.add_signal(rating_serving_signal, "rating_serving")
        self.add_transition(rating_serving_operation, rating_serving_signal, label="thread")

    @Profiling
    @Debugger
    def extract_4(self):
        """
        extract rating of hiking

        """
        input_signal = self.get_signal("input_signal")
        rating_hiking_operation = Extract(input_signal.data, "rating_hiking")
        self.add_node(rating_hiking_operation)
        self.add_transition(input_signal, rating_hiking_operation, label="thread")

        rating_hiking = rating_hiking_operation.run()
        rating_hiking_signal = Signal(rating_hiking, "Serving Hiking")

        self.add_signal(rating_hiking_signal, "rating_hiking")
        self.add_transition(rating_hiking_operation, rating_hiking_signal, label="thread")

    @Profiling
    @Debugger
    def restructure_1(self):
        """
        restructure sports statistics

        """
        sport = self.get_signal("sport")

        sport_rest_operation = RestructurePois(sport.data["sport"],
                                               "Restructure List of Sports Offers")
        self.add_node(sport_rest_operation)
        self.add_transition(sport, sport_rest_operation, label="thread")

        sport_rest = sport_rest_operation.run(col_name="Tilbud")
        sport_rest_signal = Signal(sport_rest, "Restructured List of Sports Offers")

        self.add_signal(sport_rest_signal, "sport_rest")
        self.add_transition(sport_rest_operation, sport_rest_signal)

    @Profiling
    @Debugger
    def restructure_2(self):
        """
        restructure rating of activity

        """
        activity_rating = self.get_signal("rating_activity")
        if activity_rating.data:
            activity_rating_rest_operation = RestructureRatings(
                activity_rating.data["rating_activity"], "Restructuring Activity Rating")
            self.add_node(activity_rating_rest_operation)
            self.add_transition(activity_rating, activity_rating_rest_operation, label="thread")

            activity_rating_rest = {"rating_activity": activity_rating_rest_operation.run()}
            activity_rating_rest_signal = Signal(activity_rating_rest,
                                                 "Restructured Activity Rating")

            self.add_signal(activity_rating_rest_signal, "rating_activity_rest")
            self.add_transition(activity_rating_rest_operation, activity_rating_rest_signal)
        else:
            activity_rating_rest = {"rating_activity": ""}
            activity_rating_rest_signal = Signal(activity_rating_rest,
                                                 "Restructured Transportation Rating")

            self.add_signal(activity_rating_rest_signal, "rating_activity_rest")
            self.add_transition(activity_rating, activity_rating_rest_signal)

    @Profiling
    @Debugger
    def restructure_3(self):
        """
        restructure rating of serving offers

        """
        serving_rating = self.get_signal("rating_serving")
        if serving_rating.data:
            serving_rating_rest_operation = RestructureRatings(
                serving_rating.data["rating_serving"], "Restructuring Serving Rating")
            self.add_node(serving_rating_rest_operation)
            self.add_transition(serving_rating, serving_rating_rest_operation, label="thread")

            serving_rating_rest = {"rating_serving": serving_rating_rest_operation.run()}
            serving_rating_rest_signal = Signal(serving_rating_rest, "Restructured Serving Rating")

            self.add_signal(serving_rating_rest_signal, "rating_serving_rest")
            self.add_transition(serving_rating_rest_operation, serving_rating_rest_signal)
        else:
            serving_rating_rest = {"rating_serving": ""}
            serving_rating_rest_signal = Signal(serving_rating_rest, "Restructured Serving Rating")

            self.add_signal(serving_rating_rest_signal, "rating_serving_rest")
            self.add_transition(serving_rating, serving_rating_rest_signal)

    @Profiling
    @Debugger
    def restructure_4(self):
        """
        restructure rating of hiking rating

        """
        hiking_rating = self.get_signal("rating_hiking")
        if hiking_rating.data:
            hiking_rating_rest_operation = RestructureRatings(
                hiking_rating.data["rating_hiking"], "Restructuring Hiking Rating")
            self.add_node(hiking_rating_rest_operation)
            self.add_transition(hiking_rating, hiking_rating_rest_operation, label="thread")

            hiking_rating_rest = {"rating_hiking": hiking_rating_rest_operation.run()}
            hiking_rating_rest_signal = Signal(hiking_rating_rest, "Restructured Hiking Rating")

            self.add_signal(hiking_rating_rest_signal, "rating_hiking_rest")
            self.add_transition(hiking_rating_rest_operation, hiking_rating_rest_signal)
        else:
            hiking_rating_rest = {"rating_hiking": ""}
            hiking_rating_rest_signal = Signal(hiking_rating_rest, "Restructured Hiking Rating")

            self.add_signal(hiking_rating_rest_signal, "rating_hiking_rest")
            self.add_transition(hiking_rating, hiking_rating_rest_signal)

    @Profiling
    @Debugger
    def multiplex(self):
        """
        method for multiplexing all leisure statistics

        """
        sport_rest = self.get_signal("sport_rest")
        rating_activity_rest = self.get_signal("rating_activity_rest")
        rating_serving_rest = self.get_signal("rating_serving_rest")
        rating_hiking_rest = self.get_signal("rating_hiking_rest")

        multiplex_operation = Multiplex(
            [sport_rest.data, rating_activity_rest.data, rating_serving_rest.data,
             rating_hiking_rest], desc="Multiplex Leisure Statistics")

        self.add_transition(sport_rest, multiplex_operation)
        self.add_transition(rating_activity_rest, multiplex_operation)
        self.add_transition(rating_serving_rest, multiplex_operation)
        self.add_transition(rating_hiking_rest, multiplex_operation)

        self.add_node(multiplex_operation)

        multiplex = multiplex_operation.run()
        multiplex_signal = Signal(multiplex, "Multiplexed Leisure Statistics",
                                  prettify_keys=True, length=5)
        self.add_signal(multiplex_signal, "multiplex_leisure_statistics")

        self.add_transition(multiplex_operation, multiplex_signal)

    @Profiling
    @Debugger
    def output_operation(self):
        """
        final operation of the process

        """
        multiplexed_leisure_statistics = self.get_signal("multiplex_leisure_statistics")
        output_operation = OutputOperation("Processed Leisure Statistics")
        self.add_node(output_operation)
        self.add_transition(multiplexed_leisure_statistics, output_operation)
        self.print_pdf()

        return multiplexed_leisure_statistics.data
