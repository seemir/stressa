# -*- coding: utf-8 -*-

"""
Module for the processing of Finn advert information

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Profiling

from .engine import Process, InputOperation, Signal, ScrapeFinnAdvertInfo, \
    ScrapeFinnOwnershipHistory, ScrapeFinnStatisticsInfo, Multiplex, OutputSignal, \
    OutputOperation, ValidateFinnCode, Extract, AddRowToDataFrame, PriceChange


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
        self.input_operation({"finn_code": finn_code})
        self._validated_finn_code = self.validate_finn_code()

        self._finn_advert_info = None
        self._finn_ownership_history = None
        self._finn_statistics_info = None
        self.run_parallel([self.scrape_finn_advert_info, self.scrape_finn_statistics_info,
                           self.scrape_finn_ownership_history])

        self._multiplex_info_1 = self.multiplex_1(
            [self.finn_advert_info, self.finn_ownership_history, self.finn_statistics_info])

        self.extract()
        self.add_to_dataframe()

        self._price_changes = self.price_change()
        self._multiplex_info_2 = self.multiplex_2([self.multiplex_info_1, self.price_changes])

        self.output_operation()
        self.end_process()

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
    def multiplex_info_1(self):
        """
        first multiplex info getter

        Returns
        -------
        out     : dict
                  active finn multiplex info in object

        """
        return self._multiplex_info_1

    @property
    def multiplex_info_2(self):
        """
        second multiplex info getter

        Returns
        -------
        out     : dict
                  active finn multiplex info in object

        """
        return self._multiplex_info_2

    @property
    def price_changes(self):
        """
        getter for dictionary with changes in real-estate price

        Returns
        -------

        """
        return self._price_changes

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

    @Profiling
    def validate_finn_code(self):
        """
        method for validating finn code

        """
        validate_finn_code = ValidateFinnCode(self.get_signal("input_signal").data["finn_code"])
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
            finn_owner_history_signal = Signal(finn_owner_history, "FINN Ownership History")
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
    def multiplex_1(self, signals: list):
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

        multiplex = multiplex_operation.run()
        multiplex_signal = Signal(multiplex, desc="Multiplexed Finn Information",
                                  prettify_keys=True)
        self.add_signal(multiplex_signal, "multiplexed_data")
        self.add_transition(multiplex_operation, multiplex_signal)
        return multiplex

    @Profiling
    def extract(self):
        """
        method for extracting prisantydning and history from the multiplexed dictionary

        """
        extract_price_operation = Extract(self.get_signal("multiplexed_data").data, "prisantydning")
        self.add_node(extract_price_operation)
        extract_history_operation = Extract(self.get_signal("multiplexed_data").data, "historikk")
        self.add_node(extract_history_operation)
        self.add_transition(self.get_signal("multiplexed_data"), extract_price_operation)
        self.add_transition(self.get_signal("multiplexed_data"), extract_history_operation)

        extract_price = extract_price_operation.run()
        extract_price_signal = Signal(extract_price, "List Price of Real-estate")
        extract_history = extract_history_operation.run()
        extract_history_signal = Signal(extract_history, "Ownership History")

        self.add_signal(extract_price_signal, "list_price_of_real_estate")
        self.add_signal(extract_history_signal, "ownership_history")

        self.add_transition(extract_price_operation, extract_price_signal)
        self.add_transition(extract_history_operation, extract_history_signal)

    @Profiling
    def add_to_dataframe(self):
        """
        method for adding prisantydning to ownership history dataframe

        Returns
        -------
        out             : dict
                          dictionary which can be converted to dataframe

        """
        add_row_to_dataframe_operation = AddRowToDataFrame(
            self.get_signal("list_price_of_real_estate").data,
            self.get_signal("ownership_history").data, "Add List Price to Ownership History")
        self.add_node(add_row_to_dataframe_operation)

        self.add_transition(self.get_signal("list_price_of_real_estate"),
                            add_row_to_dataframe_operation,
                            label="row")
        self.add_transition(self.get_signal("ownership_history"), add_row_to_dataframe_operation,
                            label="dataframe")

        add_row_to_dataframe = add_row_to_dataframe_operation.run()
        add_row_to_dataframe_signal = Signal(add_row_to_dataframe, "Ownership History with "
                                                                   "List Price")
        self.add_signal(add_row_to_dataframe_signal, "ownership_history_with_list_price")

        self.add_transition(add_row_to_dataframe_operation, add_row_to_dataframe_signal)

    @Profiling
    def price_change(self):
        """
        method for calculating percentage change in prices

        Returns
        -------
        out         : dict
                      dictionary with ownership history, list-prices and percentage change in price

        """
        price_change_operation = PriceChange(
            self.get_signal("ownership_history_with_list_price").data,
            "Calculate Percentage Change in Real-estate Price")
        self.add_node(price_change_operation)
        price_change = {"historikk": price_change_operation.run()}

        self.add_transition(self.get_signal("ownership_history_with_list_price"),
                            price_change_operation)

        price_change_signal = Signal(price_change, "Ownership History with Percentage Change "
                                                   "in Real-estate Price")
        self.add_signal(price_change_signal, "price_change_signal")

        self.add_transition(price_change_operation, price_change_signal)
        return price_change

    @Profiling
    def multiplex_2(self, signals):
        """
        second method for multiplexing signals

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
        multiplex_operation = Multiplex(signals, desc="Multiplex Scraped Finn Information "
                                                      "and Ownership History with List Price "
                                                      "and Price Change")
        self.add_node(multiplex_operation)
        multiplex = multiplex_operation.run()

        self.add_transition(self.get_signal("price_change_signal"), multiplex_operation)
        self.add_transition(self.get_signal("multiplexed_data"), multiplex_operation)

        multiplex_signal = Signal(multiplex, "Multiplexed Finn Information", prettify_keys=True)
        self.add_signal(multiplex_signal, "multiplex_history_data")

        self.add_transition(multiplex_operation, multiplex_signal)
        return multiplex

    @Profiling
    def output_operation(self):
        """
        final method call in process

        """
        output_operation = OutputOperation(desc="Multiplexed Finn Information")
        self.add_node(output_operation)
        self.add_transition(self.get_signal("multiplex_history_data"), output_operation)

        output_signal = OutputSignal(self.multiplex_info_1, desc="Finn Information",
                                     prettify_keys=True)
        self.add_signal(output_signal, "output_multiplex_data")
        self.add_transition(output_operation, output_signal)
