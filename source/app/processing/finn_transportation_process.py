# -*- coding: utf-8 -*-
"""
Module with the logic for the Transportation processing process

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Profiling, Tracking, Debugger

from .engine import Process, InputOperation, Signal, Extract, RestructurePois, RestructureRatings, \
    Restructure, Multiplex, OutputOperation


class FinnTransportationProcess(Process):
    """
    Process for handling transportation data from Finn advert

    """

    @Tracking
    def __init__(self, transportation_data: dict):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        transportation_data  : dict
                              dictionary with transportation statistics

        """
        super().__init__(name=self.__class__.__name__)
        self.start_process()
        self.input_operation(transportation_data)

        self.run_parallel([self.extract_1, self.extract_2, self.extract_3, self.extract_4,
                           self.extract_5, self.extract_6, self.extract_7])

        self.run_parallel([self.restructure_1, self.restructure_2, self.restructure_3,
                           self.restructure_4, self.restructure_5, self.restructure_6,
                           self.restructure_7])

        self.multiplex()

        self.transportation_statistics = self.output_operation()

        self.end_process()

    @Profiling
    @Tracking
    def input_operation(self, data: object):
        """
        initial operation of the process

        """
        Assertor.assert_data_types([data], [dict])
        input_operation = InputOperation("Transportation Statistics")
        self.add_node(input_operation)

        input_signal = Signal(data, desc="Transportation Statistics",
                              prettify_keys=True, length=4)
        self.add_signal(input_signal, "input_signal")
        self.add_transition(input_operation, input_signal)

    @Profiling
    @Debugger
    def extract_1(self):
        """
        extract transport information

        """
        input_signal = self.get_signal("input_signal")
        transport_operation = Extract(input_signal.data, "transport")
        self.add_node(transport_operation)
        self.add_transition(input_signal, transport_operation, label="thread")

        transport = transport_operation.run()
        transport_signal = Signal(transport, "Transport Information")

        self.add_signal(transport_signal, "transport")
        self.add_transition(transport_operation, transport_signal, label="thread")

    @Profiling
    @Debugger
    def extract_2(self):
        """
        extract public transportation rating information

        """
        input_signal = self.get_signal("input_signal")
        rating_public_transport_operation = Extract(input_signal.data,
                                                    "rating_public_transportation")
        self.add_node(rating_public_transport_operation)
        self.add_transition(input_signal, rating_public_transport_operation, label="thread")

        rating_public_transportation = rating_public_transport_operation.run()
        rating_public_transportation_signal = Signal(rating_public_transportation,
                                                     "Public Transportation Rating")
        self.add_signal(rating_public_transportation_signal, "rating_public_transportation")
        self.add_transition(rating_public_transport_operation,
                            rating_public_transportation_signal, label="thread")

    @Profiling
    @Debugger
    def extract_3(self):
        """
        extract primary transportation information

        """
        input_signal = self.get_signal("input_signal")
        primary_transport_operation = Extract(input_signal.data, "primarytransport")
        self.add_node(primary_transport_operation)
        self.add_transition(input_signal, primary_transport_operation, label="thread")

        primary_transportation = primary_transport_operation.run()
        primary_transportation_signal = Signal(primary_transportation,
                                               "Primary Transportation Information")
        self.add_signal(primary_transportation_signal, "primary_transportation")
        self.add_transition(primary_transport_operation,
                            primary_transportation_signal, label="thread")

    @Profiling
    @Debugger
    def extract_4(self):
        """
        extract charging information

        """
        input_signal = self.get_signal("input_signal")
        charging_operation = Extract(input_signal.data, "ladepunkt")
        self.add_node(charging_operation)
        self.add_transition(input_signal, charging_operation, label="thread")

        charging = charging_operation.run()
        charging_signal = Signal(charging, "Charging Information")
        self.add_signal(charging_signal, "charging")
        self.add_transition(charging_operation, charging_signal, label="thread")

    @Profiling
    @Debugger
    def extract_5(self):
        """
        extract parking rating information

        """
        input_signal = self.get_signal("input_signal")
        rating_parking_operation = Extract(input_signal.data, "rating_parking")
        self.add_node(rating_parking_operation)
        self.add_transition(input_signal, rating_parking_operation, label="thread")

        rating_parking = rating_parking_operation.run()
        rating_parking_signal = Signal(rating_parking, "Parking Rating")
        self.add_signal(rating_parking_signal, "rating_parking")
        self.add_transition(rating_parking_operation, rating_parking_signal, label="thread")

    @Profiling
    @Debugger
    def extract_6(self):
        """
        extract traffic rating information

        """
        input_signal = self.get_signal("input_signal")
        rating_traffic_operation = Extract(input_signal.data, "rating_traffic")
        self.add_node(rating_traffic_operation)
        self.add_transition(input_signal, rating_traffic_operation, label="thread")

        rating_traffic = rating_traffic_operation.run()
        rating_traffic_signal = Signal(rating_traffic, "Parking Rating")
        self.add_signal(rating_traffic_signal, "rating_traffic")
        self.add_transition(rating_traffic_operation, rating_traffic_signal, label="thread")

    @Profiling
    @Debugger
    def extract_7(self):
        """
        extract bysykler information

        """
        input_signal = self.get_signal("input_signal")
        bysykler_operation = Extract(input_signal.data, "bysykler")
        self.add_node(bysykler_operation)
        self.add_transition(input_signal, bysykler_operation, label="thread")

        bysykler = bysykler_operation.run()
        bysykler_signal = Signal(bysykler, "City Bikes Information")
        self.add_signal(bysykler_signal, "bysykler")
        self.add_transition(bysykler_operation, bysykler_signal, label="thread")

    @Profiling
    @Debugger
    def restructure_1(self):
        """
        restructure transportation statistics

        """
        transport = self.get_signal("transport")
        transport_rest_operation = RestructurePois(transport.data["transport"],
                                                   "Restructure List of Transportation Offers")
        self.add_node(transport_rest_operation)
        self.add_transition(transport, transport_rest_operation, label="thread")

        transport_rest = transport_rest_operation.run(col_name="Holdeplass")
        transport_rest_signal = Signal(transport_rest, "Restructured List of Transportation Offers")

        self.add_signal(transport_rest_signal, "transport_rest")
        self.add_transition(transport_rest_operation, transport_rest_signal)

    @Profiling
    @Debugger
    def restructure_2(self):
        """
        restructure rating of public transportation

        """
        rating_transportation = self.get_signal("rating_public_transportation")
        if rating_transportation.data:
            rating_transportation_rest_operation = RestructureRatings(
                rating_transportation.data["rating_public_transportation"],
                "Restructuring Transportation Rating")
            self.add_node(rating_transportation_rest_operation)
            self.add_transition(rating_transportation, rating_transportation_rest_operation,
                                label="thread")

            transportation_rating_rest = {
                "rating_transportation": rating_transportation_rest_operation.run()}
            transportation_rating_rest_signal = Signal(transportation_rating_rest,
                                                       "Restructured Transportation Rating")

            self.add_signal(transportation_rating_rest_signal, "rating_transportation_rest")
            self.add_transition(rating_transportation_rest_operation,
                                transportation_rating_rest_signal)
        else:
            transportation_rating_rest = {"rating_transportation": ""}
            transportation_rating_rest_signal = Signal(transportation_rating_rest,
                                                       "Restructured Transportation Rating")

            self.add_signal(transportation_rating_rest_signal, "rating_transportation_rest")
            self.add_transition(rating_transportation, transportation_rating_rest_signal)

    @Profiling
    @Debugger
    def restructure_3(self):
        """
        restructure of primary transportation statistics

        """
        primary_transport = self.get_signal("primary_transportation")
        primary_transport_rest_operation = Restructure(primary_transport.data["primarytransport"],
                                                       "Restructure Primary Transportation\n "
                                                       "Statistics")
        self.add_node(primary_transport_rest_operation)
        self.add_transition(primary_transport, primary_transport_rest_operation, label="thread")

        primary_transport_rest = primary_transport_rest_operation.run()
        primary_transport_rest_signal = Signal(primary_transport_rest,
                                               "Restructured Primary Transportation\n Statistics")
        self.add_signal(primary_transport_rest_signal, "primary_transportation_rest")
        self.add_transition(primary_transport_rest_operation, primary_transport_rest_signal)

    @Profiling
    @Debugger
    def restructure_4(self):
        """
        restructure of ladepunkt statistics

        """
        ladepunkt = self.get_signal("charging")
        ladepunkt_rest_operation = Restructure(ladepunkt.data["ladepunkt"],
                                               "Restructure Charging Point Statistics")
        self.add_node(ladepunkt_rest_operation)
        self.add_transition(ladepunkt, ladepunkt_rest_operation, label="thread")

        ladepunkt_rest = ladepunkt_rest_operation.run()
        ladepunkt_rest_signal = Signal(ladepunkt_rest,
                                       "Restructured Charging Point\n Statistics")
        self.add_signal(ladepunkt_rest_signal, "charging_rest")
        self.add_transition(ladepunkt_rest_operation, ladepunkt_rest_signal)

    @Profiling
    @Debugger
    def restructure_5(self):
        """
        restructure rating of parking

        """
        parking_rating = self.get_signal("rating_parking")
        if parking_rating.data:
            parking_rating_rest_operation = RestructureRatings(
                parking_rating.data["rating_parking"], "Restructuring Parking Rating")
            self.add_node(parking_rating_rest_operation)
            self.add_transition(parking_rating, parking_rating_rest_operation, label="thread")

            parking_rating_rest = {"rating_parking": parking_rating_rest_operation.run()}
            parking_rating_rest_signal = Signal(parking_rating_rest, "Restructured Parking Rating")

            self.add_signal(parking_rating_rest_signal, "rating_parking_rest")
            self.add_transition(parking_rating_rest_operation, parking_rating_rest_signal)
        else:
            parking_rating_rest = {"rating_parking": ""}
            parking_rating_rest_signal = Signal(parking_rating_rest, "Restructured Parking Rating")

            self.add_signal(parking_rating_rest_signal, "rating_parking_rest")
            self.add_transition(parking_rating, parking_rating_rest_signal)

    @Profiling
    @Debugger
    def restructure_6(self):
        """
        restructure rating of traffic

        """
        traffic_rating = self.get_signal("rating_traffic")
        if traffic_rating.data:
            traffic_rating_rest_operation = RestructureRatings(
                traffic_rating.data["rating_traffic"], "Restructuring Traffic Rating")
            self.add_node(traffic_rating_rest_operation)
            self.add_transition(traffic_rating, traffic_rating_rest_operation, label="thread")

            traffic_rating_rest = {"rating_traffic": traffic_rating_rest_operation.run()}
            traffic_rating_rest_signal = Signal(traffic_rating_rest, "Restructured Traffic Rating")

            self.add_signal(traffic_rating_rest_signal, "rating_traffic_rest")
            self.add_transition(traffic_rating_rest_operation, traffic_rating_rest_signal)
        else:
            traffic_rating_rest = {"rating_traffic": ""}
            traffic_rating_rest_signal = Signal(traffic_rating_rest, "Restructured Traffic Rating")

            self.add_signal(traffic_rating_rest_signal, "rating_traffic_rest")
            self.add_transition(traffic_rating, traffic_rating_rest_signal)

    @Profiling
    @Debugger
    def restructure_7(self):
        """
        restructure city bikes statistics

        """
        city_bikes = self.get_signal("bysykler")
        if city_bikes.data:
            city_bikes_rest_operation = RestructureRatings(
                city_bikes.data["bysykler"], "Restructuring City Bikes Statistics")
            self.add_node(city_bikes_rest_operation)
            self.add_transition(city_bikes, city_bikes_rest_operation, label="thread")

            city_bikes_rest = {"bysykler": city_bikes_rest_operation.run()}
            city_bikes_rest_signal = Signal(city_bikes_rest, "Restructured City Bikes Statistics")

            self.add_signal(city_bikes_rest_signal, "bysykler_rest")
            self.add_transition(city_bikes_rest_operation, city_bikes_rest_signal)
        else:
            city_bikes_rest = {"bysykler": ""}
            city_bikes_rest_signal = Signal(city_bikes_rest, "Restructured Traffic Rating")

            self.add_signal(city_bikes_rest_signal, "bysykler_rest")
            self.add_transition(city_bikes, city_bikes_rest_signal)

    @Profiling
    @Debugger
    def multiplex(self):
        """
        method for multiplexing all transportation statistics

        """
        transport_rest = self.get_signal("transport_rest")
        transportation_rating_rest = self.get_signal("rating_transportation_rest")
        primary_transportation_rest = self.get_signal("primary_transportation_rest")
        charging_rest = self.get_signal("charging_rest")
        rating_parking_rest = self.get_signal("rating_parking_rest")
        rating_traffic_rest = self.get_signal("rating_traffic_rest")
        bysykler_rest = self.get_signal("bysykler_rest")

        multiplex_operation = Multiplex([transport_rest.data, transportation_rating_rest.data,
                                         primary_transportation_rest.data, charging_rest.data,
                                         rating_parking_rest.data, rating_traffic_rest.data,
                                         bysykler_rest.data], desc="Multiplex Transportation "
                                                                   "Statistics")

        self.add_transition(transport_rest, multiplex_operation)
        self.add_transition(transportation_rating_rest, multiplex_operation)
        self.add_transition(primary_transportation_rest, multiplex_operation)
        self.add_transition(charging_rest, multiplex_operation)
        self.add_transition(rating_parking_rest, multiplex_operation)
        self.add_transition(rating_traffic_rest, multiplex_operation)
        self.add_transition(bysykler_rest, multiplex_operation)

        self.add_node(multiplex_operation)

        multiplex = multiplex_operation.run()
        multiplex_signal = Signal(multiplex, "Multiplexed Transportation Statistics",
                                  prettify_keys=True, length=5)
        self.add_signal(multiplex_signal, "multiplex_transportation_statistics")

        self.add_transition(multiplex_operation, multiplex_signal)

    @Profiling
    @Debugger
    def output_operation(self):
        """
        final operation of the process

        """
        multiplexed_transportation_statistics = self.get_signal(
            "multiplex_transportation_statistics")
        output_operation = OutputOperation("Processed Transportation Statistics")
        self.add_node(output_operation)
        self.add_transition(multiplexed_transportation_statistics, output_operation)
        self.print_pdf()

        return multiplexed_transportation_statistics.data
