# -*- coding: utf-8 -*-

"""
Module for the processing of Finn advert information

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Profiling

from .engine import Process, InputOperation, Signal, ScrapeFinnAdvertInfo, \
    ScrapeFinnOwnershipHistory, \
    ScrapeFinnStatisticsInfo, Multiplex, OutputSignal, OutputOperation, ValidateFinnCode


class FinnAdvertProcessing(Process):
    """
    Process for processing Finn advert information

    """

    def __init__(self, finn_code: str):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        finn_code   : str
                      Finn-code to be search finn-advert information

        """
        super().__init__(name=self.__class__.__name__)
        self.start_process()
        Assertor.assert_data_types([finn_code], [str])
        self._finn_code = self.input_operation({"finn_code": finn_code})
        self._validated_finn_code = self.validate_finn_code(self.finn_code)

        self._finn_advert_info = None
        self._finn_ownership_history = None
        self._finn_statistics_info = None
        self.run_parallel([self.scrape_finn_advert_info, self.scrape_finn_statistics_info,
                           self.scrape_finn_ownership_history])

        self._multiplex_info = self.multiplex(
            [self.finn_advert_info, self.finn_ownership_history, self.finn_statistics_info])
        self.output_operation()
        self.end_process()

    @property
    def finn_code(self):
        """
        finn code getter

        Returns
        -------
        out     : dict
                  active finn-code in object

        """
        return self._finn_code

    @property
    def validated_finn_code(self):
        """
        validated finn code getter

        Returns
        -------
        out     : dict
                  active validated finn-code in object

        """
        return self._validated_finn_code

    @property
    def finn_advert_info(self):
        """
        finn advert info getter

        Returns
        -------
        out     : dict
                  active finn advert info in object

        """
        return self._finn_advert_info

    @property
    def finn_ownership_history(self):
        """
        finn advert info getter

        Returns
        -------
        out     : dict
                  active finn ownership info in object

        """
        return self._finn_ownership_history

    @property
    def finn_statistics_info(self):
        """
        finn statistics getter

        Returns
        -------
        out     : dict
                  active finn statistics info in object

        """
        return self._finn_statistics_info

    @property
    def multiplex_info(self):
        """
        multiplex info getter

        Returns
        -------
        out     : dict
                  active finn multiplex info in object

        """
        return self._multiplex_info

    @Profiling
    def input_operation(self, data: dict):
        """
        method for assigning finn code to finn processing object

        Parameters
        ----------
        data             : dict
                           finn_code sent in to process

        Returns
        -------
        out              : dict
                           finn_code saved to object

        """
        Assertor.assert_data_types([data], [dict])

        input_operation = InputOperation("FINN Code")
        self.add_node(input_operation)

        input_signal = Signal(data, desc="FINN Code")
        self.add_signal(input_signal, "input_signal")

        self.add_transition(input_operation, input_signal)
        return data

    @Profiling
    def validate_finn_code(self, data: dict):
        """
        method for validating finn code

        Parameters
        ----------
        data       : dict
                     finn_code to be validated

        Returns
        -------
        out         : dict
                      validated finn_code

        """
        Assertor.assert_data_types([data], [dict])
        validate_finn_code = ValidateFinnCode(data["finn_code"])
        self.add_node(validate_finn_code)

        self.add_transition(self.get_signal("input_signal"), validate_finn_code)

        validated_finn_code = {"finn_code": validate_finn_code.run()}
        validated_finn_code_signal = Signal(validated_finn_code, "Validated Finn Code")
        self.add_signal(validated_finn_code_signal, "validated_finn_code")

        self.add_transition(validate_finn_code, validated_finn_code_signal)
        return validated_finn_code

    @Profiling
    def scrape_finn_advert_info(self):
        """
        method for scraping finn advert info in finn-processing

        """
        try:
            scrape_finn_ad_operation = ScrapeFinnAdvertInfo(self._validated_finn_code["finn_code"])
            self.add_node(scrape_finn_ad_operation)

            self.add_transition(self.get_signal("validated_finn_code"), scrape_finn_ad_operation,
                                label="thread")

            finn_ad_info = scrape_finn_ad_operation.run()
            finn_ad_info_signal = Signal(finn_ad_info, "FINN Advert Information",
                                         prettify_keys=True)
            self.add_signal(finn_ad_info_signal, "finn_ad_info")

            self.add_transition(scrape_finn_ad_operation, finn_ad_info_signal,
                                label="thread")
            self._finn_advert_info = finn_ad_info
        except Exception as scrape_finn_ad_info_exception:
            self.exception_queue.put(scrape_finn_ad_info_exception)
            raise scrape_finn_ad_info_exception

    @Profiling
    def scrape_finn_ownership_history(self):
        """
        method for scraping finn ownership history in finn-processing

        """
        try:
            scrape_finn_owner_history = ScrapeFinnOwnershipHistory(
                self._validated_finn_code["finn_code"])
            self.add_node(scrape_finn_owner_history)

            self.add_transition(self.get_signal("validated_finn_code"), scrape_finn_owner_history,
                                label="thread")

            finn_owner_history = scrape_finn_owner_history.run()
            finn_owner_history_signal = Signal(finn_owner_history, "FINN Owner History")
            self.add_signal(finn_owner_history_signal, "finn_owner_history")

            self.add_transition(scrape_finn_owner_history, finn_owner_history_signal,
                                label="thread")
            self._finn_ownership_history = finn_owner_history
        except Exception as scrape_finn_ownership_history_exception:
            self.exception_queue.put(scrape_finn_ownership_history_exception)
            raise scrape_finn_ownership_history_exception

    @Profiling
    def scrape_finn_statistics_info(self):
        """
        method for scraping finn statistics info in finn-processing

        """
        try:
            scrape_finn_stat_operation = ScrapeFinnStatisticsInfo(
                self._validated_finn_code["finn_code"])
            self.add_node(scrape_finn_stat_operation)

            self.add_transition(self.get_signal("validated_finn_code"), scrape_finn_stat_operation,
                                label="thread")

            finn_stat_info = scrape_finn_stat_operation.run()
            finn_stat_info_signal = Signal(finn_stat_info, "FINN Statistics Information")
            self.add_signal(finn_stat_info_signal, "finn_stat_info")

            self.add_transition(scrape_finn_stat_operation, finn_stat_info_signal,
                                label="thread")
            self._finn_statistics_info = finn_stat_info
        except Exception as scrape_finn_statistics_info_exception:
            self.exception_queue.put(scrape_finn_statistics_info_exception)
            raise scrape_finn_statistics_info_exception

    @Profiling
    def multiplex(self, signals: list):
        """
        method for multiplexing signals

        Parameters
        ----------
        signals     : list
                      list of Signal objects

        Returns
        -------
        dict        : dict
                      dictionary with all signal information in one dict

        """
        Assertor.assert_data_types([signals], [list])
        multiplex_operation = Multiplex(signals, desc="Multiplex Scraped Finn Information")
        self.add_node(multiplex_operation)

        self.add_transition(self.get_signal("finn_ad_info"), multiplex_operation)
        self.add_transition(self.get_signal("finn_owner_history"), multiplex_operation)
        self.add_transition(self.get_signal("finn_stat_info"), multiplex_operation)

        multiplex_data = multiplex_operation.run()
        multiplex_signal = Signal(multiplex_data, desc="Multiplexed Finn Information",
                                  prettify_keys=True)
        self.add_signal(multiplex_signal, "multiplexed_data")
        self.add_transition(multiplex_operation, multiplex_signal)
        return multiplex_data

    @Profiling
    def output_operation(self):
        """
        final method call in process

        """
        output_operation = OutputOperation(desc="Multiplexed Finn Information")
        self.add_node(output_operation)
        self.add_transition(self.get_signal("multiplexed_data"), output_operation)

        output_signal = OutputSignal(self.multiplex_info, desc="Finn Information",
                                     prettify_keys=True)
        self.add_signal(output_signal, "output_multiplex_data")
        self.add_transition(output_operation, output_signal)
