# -*- coding: utf-8 -*-

"""
Module for the processing of Finn information

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Profiling

from .engine import Process, InputOperation, Signal, ScrapeFinnAdInfo, ScrapeFinnOwnershipHistory, \
    ScrapeFinnStatisticsInfo, Multiplex, OutputSignal, OutputOperation, ValidateFinnCode


class FinnProcessing(Process):
    """
    Process for getting Finn information

    """

    def __init__(self, finn_code: str):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        finn_code   : str
                      Finn-code to be search finn-ad information

        """
        super().__init__(name=self.__class__.__name__)
        self.start_process()
        Assertor.assert_data_types([finn_code], [str])
        self._finn_code = self.input_operation({"finn_code": finn_code})
        self._validated_finn_code = self.validate_finn_code(self.finn_code)

        self._finn_ad_info = None
        self._finn_ownership_history = None
        self._finn_statistics_info = None
        self.run_parallel([self.scrape_finn_ad_info, self.scrape_finn_statistics_info,
                           self.scrape_finn_ownership_history])

        self._multiplex_info = self.multiplex(
            [self.finn_ad_info, self.finn_ownership_history, self.finn_statistics_info])
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
    def finn_ad_info(self):
        """
        finn ad info getter

        Returns
        -------
        out     : dict
                  active finn ad info in object

        """
        return self._finn_ad_info

    @property
    def finn_ownership_history(self):
        """
        finn ad info getter

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
    def scrape_finn_ad_info(self):
        """
        method for scraping finn ad info in finn-processing

        """
        scrape_finn_ad_operation = ScrapeFinnAdInfo(self._validated_finn_code["finn_code"])
        self.add_node(scrape_finn_ad_operation)

        self.add_transition(self.get_signal("validated_finn_code"), scrape_finn_ad_operation)

        finn_ad_info = scrape_finn_ad_operation.run()
        finn_ad_info_signal = Signal(finn_ad_info, "FINN AD Information", prettify_keys=True)
        self.add_signal(finn_ad_info_signal, "finn_ad_info")

        self.add_transition(scrape_finn_ad_operation, finn_ad_info_signal)
        self._finn_ad_info = finn_ad_info

    @Profiling
    def scrape_finn_ownership_history(self):
        """
        method for scraping finn ownership history in finn-processing

        """
        scrape_finn_owner_history = ScrapeFinnOwnershipHistory(
            self._validated_finn_code["finn_code"])
        self.add_node(scrape_finn_owner_history)

        self.add_transition(self.get_signal("validated_finn_code"), scrape_finn_owner_history)

        finn_owner_history = scrape_finn_owner_history.run()
        finn_owner_history_signal = Signal(finn_owner_history, "FINN Owner History")
        self.add_signal(finn_owner_history_signal, "finn_owner_history")

        self.add_transition(scrape_finn_owner_history, finn_owner_history_signal)
        self._finn_ownership_history = finn_owner_history

    @Profiling
    def scrape_finn_statistics_info(self):
        """
        method for scraping finn statistics info in finn-processing

        """
        scrape_finn_stat_operation = ScrapeFinnStatisticsInfo(
            self._validated_finn_code["finn_code"])
        self.add_node(scrape_finn_stat_operation)

        self.add_transition(self.get_signal("validated_finn_code"), scrape_finn_stat_operation)

        finn_stat_info = scrape_finn_stat_operation.run()
        finn_stat_info_signal = Signal(finn_stat_info, "FINN Statistics Information")
        self.add_signal(finn_stat_info_signal, "finn_stat_info")

        self.add_transition(scrape_finn_stat_operation, finn_stat_info_signal)
        self._finn_statistics_info = finn_stat_info

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
        output_operation = OutputOperation(desc="id: Multiplexed Finn Information")
        self.add_node(output_operation)
        self.add_transition(self.get_signal("multiplexed_data"), output_operation)

        output_signal = OutputSignal(self.multiplex_info, desc="Finn Information",
                                     prettify_keys=True)
        self.add_signal(output_signal, "output_multiplex_data")
        self.add_transition(output_operation, output_signal)
        return self.multiplex_info
