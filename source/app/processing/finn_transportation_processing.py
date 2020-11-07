# -*- coding: utf-8 -*-
"""
Module with the logic for the Transportation processing process

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Profiling, Tracking, Debugger

from .engine import Process, InputOperation, Signal, Extract


class FinnTransportationProcessing(Process):
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

        self.transportation_statistics = self.output_operation()

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
    def output_operation(self):
        """
        final operation of the process

        """
        self.print_pdf()
