# -*- coding: utf-8 -*-

"""
Module for the processing of Finn advert information

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Profiling, Tracking, Debugger, LOGGER

from .engine import Process, InputOperation, Signal, ScrapeFinnAdvertInfo, \
    ScrapeFinnOwnershipHistory, ScrapeFinnStatisticsInfo, Multiplex, OutputSignal, \
    OutputOperation, ValidateFinnCode, Extract, AddRowToDataFrame, RateOfChange, \
    ExtractFirstRow, CheckNewestDate, Accumulate, ScrapeFinnCommunityStatistics

from .finn_community_sub_model import FinnCommunitySubModel


class FinnAdvertProcessing(Process):
    """
    Process for processing Finn advert information

    """

    @Tracking
    def __init__(self, finn_code: str):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        finn_code   : str
                      Finn-code to be search finn-advert information

        """
        self.start_process()
        super().__init__(name=self.__class__.__name__)
        Assertor.assert_data_types([finn_code], [str])
        self.input_operation({"finn_code": finn_code})
        self.validate_finn_code()
        self.run_parallel([self.scrape_finn_statistics_info,
                           self.scrape_finn_community_statistics,
                           self.scrape_finn_advert_info,
                           self.scrape_finn_ownership_history])

        self._multiplex_info_1 = self.multiplex_1()

        self.run_parallel([self.extract_1, self.extract_2, self.extract_3,
                           self.extract_4, self.extract_5])

        self.run_parallel([self.extract_first_row, self.add_to_dataframe_1,
                           self.rate_of_change_1, self.finn_community_process])

        self.run_parallel([self.check_newest_date, self.accumulate])

        self.run_parallel([self.add_to_dataframe_2, self.multiplex_2])

        self.rate_of_change_2()
        self._multiplex_info_2 = self.multiplex_3()
        self.output_operation()
        self.end_process()

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

    @Profiling
    @Tracking
    def input_operation(self, data: dict):
        """
        initial operation in process

        Parameters
        ----------
        data             : dict
                           finn_code sent in to process

        Returns
        -------
        out              : dict
                           finn_code saved as signal

        """
        Assertor.assert_data_types([data], [dict])

        input_operation = InputOperation("FINN Code")
        self.add_node(input_operation)

        input_signal = Signal(data, desc="FINN Code")
        self.add_signal(input_signal, "input_signal")

        self.add_transition(input_operation, input_signal)

    @Profiling
    @Tracking
    def validate_finn_code(self):
        """
        method for validating finn code

        """
        input_signal = self.get_signal("input_signal")
        validate_finn_code = ValidateFinnCode(input_signal.data["finn_code"])
        self.add_node(validate_finn_code)

        self.add_transition(input_signal, validate_finn_code)

        validated_finn_code = {"finn_code": validate_finn_code.run()}
        validated_finn_code_signal = Signal(validated_finn_code, "Validated Finn Code")
        self.add_signal(validated_finn_code_signal, "validated_finn_code")

        self.add_transition(validate_finn_code, validated_finn_code_signal)

    @Profiling
    @Tracking
    def scrape_finn_advert_info(self):
        """
        method for scraping finn advert info in finn-processing

        """
        try:
            validated_finn_code = self.get_signal("validated_finn_code")
            scrape_finn_ad_operation = ScrapeFinnAdvertInfo(validated_finn_code.data["finn_code"])
            self.add_node(scrape_finn_ad_operation)

            self.add_transition(validated_finn_code, scrape_finn_ad_operation, label="thread")

            finn_ad_info = scrape_finn_ad_operation.run()
            finn_ad_info_signal = Signal(finn_ad_info, "FINN Advert Information",
                                         prettify_keys=True, length=9)
            self.add_signal(finn_ad_info_signal, "finn_ad_info")

            self.add_transition(scrape_finn_ad_operation, finn_ad_info_signal,
                                label="thread")
        except Exception as scrape_finn_ad_info_exception:
            self.exception_queue.put(scrape_finn_ad_info_exception)
            raise scrape_finn_ad_info_exception

    @Profiling
    @Tracking
    def scrape_finn_ownership_history(self):
        """
        method for scraping finn ownership history in finn-processing

        """
        try:
            validated_finn_code = self.get_signal("validated_finn_code")
            scrape_finn_owner_history = ScrapeFinnOwnershipHistory(
                validated_finn_code.data["finn_code"])
            self.add_node(scrape_finn_owner_history)
            self.add_transition(validated_finn_code, scrape_finn_owner_history,
                                label="thread")
            finn_owner_history = scrape_finn_owner_history.run()
            finn_owner_history_signal = Signal(finn_owner_history, "FINN Ownership History")
            self.add_signal(finn_owner_history_signal, "finn_owner_history")

            self.add_transition(scrape_finn_owner_history, finn_owner_history_signal,
                                label="thread")
        except Exception as scrape_finn_ownership_history_exception:
            self.exception_queue.put(scrape_finn_ownership_history_exception)
            raise scrape_finn_ownership_history_exception

    @Profiling
    @Tracking
    def scrape_finn_statistics_info(self):
        """
        method for scraping finn view statistics info in finn-processing

        """
        try:
            validated_finn_code = self.get_signal("validated_finn_code")
            scrape_finn_stat_operation = ScrapeFinnStatisticsInfo(
                validated_finn_code.data["finn_code"])
            self.add_node(scrape_finn_stat_operation)

            self.add_transition(validated_finn_code, scrape_finn_stat_operation, label="thread")

            finn_stat_info = scrape_finn_stat_operation.run()
            finn_stat_info_signal = Signal(finn_stat_info, "FINN Statistics Information",
                                           prettify_keys=True, length=6)
            self.add_signal(finn_stat_info_signal, "finn_stat_info")

            self.add_transition(scrape_finn_stat_operation, finn_stat_info_signal,
                                label="thread")
        except Exception as scrape_finn_statistics_info_exception:
            self.exception_queue.put(scrape_finn_statistics_info_exception)
            raise scrape_finn_statistics_info_exception

    @Profiling
    @Tracking
    def scrape_finn_community_statistics(self):
        """
        method for scraping finn community statistics

        """
        try:
            validated_finn_code = self.get_signal("validated_finn_code")
            scrape_finn_community_statistics_operation = ScrapeFinnCommunityStatistics(
                validated_finn_code.data["finn_code"])
            self.add_node(scrape_finn_community_statistics_operation)

            self.add_transition(validated_finn_code, scrape_finn_community_statistics_operation,
                                label="thread")
            finn_community_statistics = scrape_finn_community_statistics_operation.run()
            finn_community_statistics_signal = Signal(finn_community_statistics,
                                                      "FINN Community Statistics",
                                                      prettify_keys=True, length=6)
            self.add_signal(finn_community_statistics_signal, "finn_community_statistics")

            self.add_transition(scrape_finn_community_statistics_operation,
                                finn_community_statistics_signal, label="thread")
        except Exception as scrape_finn_community_statistics_exception:
            self.exception_queue.put(scrape_finn_community_statistics_exception)
            raise scrape_finn_community_statistics_exception

    @Profiling
    @Tracking
    def multiplex_1(self):
        """
        method for multiplexing signals

        """
        finn_ad_info = self.get_signal("finn_ad_info")
        finn_owner_history = self.get_signal("finn_owner_history")
        finn_stat_info = self.get_signal("finn_stat_info")
        finn_community_stat = self.get_signal("finn_community_statistics")

        signals = [finn_ad_info, finn_owner_history, finn_stat_info, finn_community_stat]
        multiplex_operation = Multiplex(signals, desc="Multiplex Scraped Finn Information")
        self.add_node(multiplex_operation)

        self.add_transition(finn_ad_info, multiplex_operation)
        self.add_transition(finn_owner_history, multiplex_operation)
        self.add_transition(finn_stat_info, multiplex_operation)
        self.add_transition(finn_community_stat, multiplex_operation)

        multiplex = multiplex_operation.run()
        multiplex_signal = Signal(multiplex, desc="Multiplexed Finn Information",
                                  prettify_keys=True, length=9)
        self.add_signal(multiplex_signal, "multiplexed_data")
        self.add_transition(multiplex_operation, multiplex_signal)
        return multiplex

    @Profiling
    @Tracking
    def extract_1(self):
        """
        method for extracting published date

        """
        try:
            multiplexed_data = self.get_signal("multiplexed_data")

            extract_published_date_operation = Extract(multiplexed_data.data, "published")
            self.add_node(extract_published_date_operation)
            self.add_transition(multiplexed_data, extract_published_date_operation, label="thread")

            extract_published_date = extract_published_date_operation.run()
            extract_published_date_signal = Signal(extract_published_date,
                                                   "Publishing Date of Advertisement")
            self.add_signal(extract_published_date_signal, "publish_date")

            self.add_transition(extract_published_date_operation, extract_published_date_signal,
                                label="thread")
        except Exception as extract_exception:
            self.exception_queue.put(extract_exception)
            raise extract_exception

    @Profiling
    @Tracking
    def extract_2(self):
        """
        method for extracting price of real-estate

        """
        try:
            multiplexed_data = self.get_signal("multiplexed_data")

            extract_price_operation = Extract(multiplexed_data.data, "prisantydning")
            self.add_node(extract_price_operation)
            self.add_transition(multiplexed_data, extract_price_operation, label="thread")

            extract_price = extract_price_operation.run()
            extract_price_signal = Signal(extract_price, "List Price of Real-estate")
            self.add_signal(extract_price_signal, "list_price_of_real_estate")

            self.add_transition(extract_price_operation, extract_price_signal, label="thread")
        except Exception as extract_exception:
            self.exception_queue.put(extract_exception)
            raise extract_exception

    @Profiling
    @Tracking
    def extract_3(self):
        """
        method for extracting sales history

        """
        try:
            multiplexed_data = self.get_signal("multiplexed_data")

            extract_history_operation = Extract(multiplexed_data.data, "historikk")
            self.add_node(extract_history_operation)
            self.add_transition(multiplexed_data, extract_history_operation, label="thread")

            extract_history = extract_history_operation.run()
            extract_history_signal = Signal(extract_history, "Ownership History")
            self.add_signal(extract_history_signal, "ownership_history")

            self.add_transition(extract_history_operation, extract_history_signal, label="thread")
        except Exception as extract_exception:
            self.exception_queue.put(extract_exception)
            raise extract_exception

    @Profiling
    @Tracking
    def extract_4(self):
        """
        method for extracting view development statistics

        """
        try:
            multiplexed_data = self.get_signal("multiplexed_data")

            extract_views_development_operation = Extract(multiplexed_data.data,
                                                          "views_development")
            self.add_node(extract_views_development_operation)
            self.add_transition(multiplexed_data, extract_views_development_operation,
                                label="thread")

            extract_views_development = extract_views_development_operation.run()
            extract_views_development_signal = Signal(extract_views_development,
                                                      "Development of Advert Views")
            self.add_signal(extract_views_development_signal, "views_development")

            self.add_transition(extract_views_development_operation,
                                extract_views_development_signal,
                                label="thread")
        except Exception as extract_exception:
            self.exception_queue.put(extract_exception)
            raise extract_exception

    @Profiling
    @Tracking
    def extract_5(self):
        """
        method for extracting community json

        """
        try:
            multiplexed_data = self.get_signal("multiplexed_data")

            extract_community_data_operation = Extract(multiplexed_data.data, "nabolag")
            self.add_node(extract_community_data_operation)
            self.add_transition(multiplexed_data, extract_community_data_operation, label="thread")

            extract_community_data = extract_community_data_operation.run()
            extract_community_data_signal = Signal(extract_community_data,
                                                   "Finn Community Statistics")
            self.add_signal(extract_community_data_signal, "community_data")

            self.add_transition(extract_community_data_operation, extract_community_data_signal,
                                label="thread")
        except Exception as extract_exception:
            self.exception_queue.put(extract_exception)
            raise extract_exception

    @Profiling
    @Debugger
    def extract_first_row(self):
        """
        method for extracting first row from ownership history

        """
        try:
            extract_first_row_operation = ExtractFirstRow(self.get_signal("ownership_history").data,
                                                          "Extract the Newest Sale with Date")
            self.add_node(extract_first_row_operation)
            self.add_transition(self.get_signal("ownership_history"), extract_first_row_operation,
                                label="thread")

            extract_first_row = extract_first_row_operation.run()
            extract_first_row_signal = Signal(extract_first_row, "Newest Sale with Date")
            self.add_signal(extract_first_row_signal, "extracted_first_row")
            self.add_transition(extract_first_row_operation, extract_first_row_signal,
                                label="thread")
        except Exception as extract_first_row_exception:
            self.exception_queue.put(extract_first_row_exception)

    @Profiling
    @Debugger
    def add_to_dataframe_1(self):
        """
        method for adding prisantydning to ownership history dataframe

        """
        try:
            add_row_to_dataframe_operation = AddRowToDataFrame(
                self.get_signal("list_price_of_real_estate").data,
                self.get_signal("ownership_history").data, "Add List Price to Ownership History")
            self.add_node(add_row_to_dataframe_operation)

            self.add_transition(self.get_signal("list_price_of_real_estate"),
                                add_row_to_dataframe_operation,
                                label="row", thread=True)
            self.add_transition(self.get_signal("ownership_history"),
                                add_row_to_dataframe_operation,
                                label="dataframe", thread=True)

            add_row_to_dataframe = add_row_to_dataframe_operation.run()
            add_row_to_dataframe_signal = Signal(add_row_to_dataframe, "Ownership History with "
                                                                       "List Price")
            self.add_signal(add_row_to_dataframe_signal, "ownership_history_with_list_price")

            self.add_transition(add_row_to_dataframe_operation, add_row_to_dataframe_signal,
                                label="thread")
        except Exception as add_to_dateframe_exception:
            self.exception_queue.put(add_to_dateframe_exception)

    @Profiling
    @Debugger
    def rate_of_change_1(self):
        """
        method for calculating rate of change in views vector

        """
        try:
            views_development = self.get_signal("views_development")
            try:
                total = views_development.data["views_development"]["total_views"][::-1]
                views_development.data["views_development"].update({"total_views": total})

                rate_of_change_operation = RateOfChange(
                    views_development.data["views_development"],
                    "Calculate Percentage Change in Advert Views")

                self.add_node(rate_of_change_operation)
                self.add_transition(views_development, rate_of_change_operation, label="thread")

                rate_of_change = rate_of_change_operation.run()

                index = list(rate_of_change["total_views"].keys())
                total = list(rate_of_change["total_views"].values())[::-1]
                change = list(rate_of_change["Endring"].values())[::-1]

                rate_of_change.update({"total_views": dict(zip(index, total))})
                rate_of_change.update({"Endring": dict(zip(index, change))})
                rate_of_change["change"] = rate_of_change["Endring"]
                del rate_of_change["Endring"]

                rate_of_change_signal = Signal({"views_development": rate_of_change},
                                               "Percentage Change in Advert Views")

                self.add_signal(rate_of_change_signal, "views_change_signal")
                self.add_transition(rate_of_change_operation, rate_of_change_signal, label="thread")
            except Exception as no_view_statistics_error:
                LOGGER.debug(
                    "[{}.rate_of_change_1] No view statistics found!, exited with '{}'".format(
                        self.__class__.__name__, no_view_statistics_error))
        except Exception as rate_of_change_exception:
            self.exception_queue.put(rate_of_change_exception)

    @Profiling
    @Debugger
    def finn_community_process(self):
        """
        method for processing community statistics data from Finn

        """
        try:
            community_json = self.get_signal("community_data")

            process_community_data_operation = FinnCommunitySubModel(community_json.data)
            self.add_node(process_community_data_operation)
            self.add_transition(community_json, process_community_data_operation, label="thread")

            process_community_data = process_community_data_operation.run()

            process_community_data_signal = Signal(process_community_data,
                                                   "Processed Finn Community Statistics",
                                                   prettify_keys=True, length=5)
            self.add_signal(process_community_data_signal, "processed_community_data")
            self.add_transition(process_community_data_operation, process_community_data_signal,
                                label="thread")
        except Exception as finn_community_exception:
            self.exception_queue.put(finn_community_exception)

    @Profiling
    @Debugger
    def check_newest_date(self):
        """
        method for checking which of two dates are the newest date

        """
        try:
            publish_date = self.get_signal("publish_date")
            extracted_first_row = self.get_signal("extracted_first_row")
            check_newest_date_operation = CheckNewestDate(publish_date.data,
                                                          extracted_first_row.data,
                                                          "Publishing Date of Advertisement Later "
                                                          "Than Newest Sale")
            self.add_node(check_newest_date_operation)
            self.add_transition(publish_date, check_newest_date_operation, label="thread")
            self.add_transition(extracted_first_row, check_newest_date_operation, label="thread")

            check_newest_date = check_newest_date_operation.run()
            self.signal.update({"sold": check_newest_date})

            not_sold_signal = Signal(extracted_first_row.data,
                                     desc="Advertised Real-Estate Not Sold / Registered Yet")
            final_sales_price = Signal(extracted_first_row.data,
                                       desc="Final Sales Price of Advertised Real-Estate")

            self.add_signal(not_sold_signal, "not_sold")
            self.add_signal(final_sales_price, "final_sales_price")
            self.add_transition(check_newest_date_operation, final_sales_price, label="true",
                                thread=True)
            self.add_transition(check_newest_date_operation, not_sold_signal, label="false",
                                thread=True)
        except Exception as check_newest_date_exception:
            self.exception_queue.put(check_newest_date_exception)

    @Profiling
    @Debugger
    def accumulate(self):
        """
        method for accumulating the values in dataframe column

        """
        try:
            views_development = self.get_signal("views_change_signal")
            try:
                total = dict([[*views_development.data["views_development"].items()][3]])
                accumulate_operation = Accumulate(total, "Calculate the Accumulated Sum of Views")

                self.add_node(accumulate_operation)
                self.add_transition(views_development, accumulate_operation, label="thread")

                accumulate = accumulate_operation.run()

                accumulate_signal = Signal(accumulate, "Accumulated Sum of Views")
                self.add_signal(accumulate_signal, "accumulated_signal")
                self.add_transition(accumulate_operation, accumulate_signal, label="thread")
            except Exception as no_view_statistics_error:
                LOGGER.debug(
                    "[{}.accumulate] Accumulate not possible!, exited with '{}'".format(
                        self.__class__.__name__, no_view_statistics_error))
        except Exception as accumulate_exception:
            self.exception_queue.put(accumulate_exception)

    @Profiling
    @Debugger
    def add_to_dataframe_2(self):
        """
        method for adding final sales price (if sold) to ownership history dataframe

        """
        try:
            sales_price = self.get_signal("final_sales_price")
            ownership_history = self.get_signal("ownership_history_with_list_price")
            if self.get_signal("sold"):
                add_row_to_dataframe_operation = AddRowToDataFrame(
                    sales_price.data, ownership_history.data,
                    desc="Add Final Sales Price to to Ownership History")
            else:
                add_row_to_dataframe_operation = AddRowToDataFrame(
                    row=None,
                    dataframe=ownership_history.data,
                    desc="Add Final Sales Price to Ownership History")
            self.add_node(add_row_to_dataframe_operation)
            self.add_transition(sales_price, add_row_to_dataframe_operation, label="row",
                                thread=True)
            self.add_transition(ownership_history, add_row_to_dataframe_operation,
                                label="dataframe", thread=True)

            add_row_to_dataframe = add_row_to_dataframe_operation.run()
            add_row_to_dataframe_signal = Signal(add_row_to_dataframe,
                                                 "Ownership History With List "
                                                 "Price and Final Sales Price")
            self.add_signal(add_row_to_dataframe_signal, "final_ownership_history")
            self.add_transition(add_row_to_dataframe_operation, add_row_to_dataframe_signal,
                                label="thread")
        except Exception as add_to_dateframe_exception:
            self.exception_queue.put(add_to_dateframe_exception)

    @Profiling
    @Debugger
    def multiplex_2(self):
        """
        multiplexing the accumulated sum of views with the views development

        """
        try:
            views_development = self.get_signal("views_change_signal")
            accumulated = self.get_signal("accumulated_signal")
            try:
                multiplex_operation = Multiplex(
                    [views_development.data["views_development"], accumulated],
                    "Multiplex Accumulated Sum with Views Development")
                self.add_node(multiplex_operation)
                self.add_transition(views_development, multiplex_operation, label="thread")
                self.add_transition(accumulated, multiplex_operation, label="thread")

                multiplex = {"views_development": multiplex_operation.run()}
                multiplex_signal = Signal(multiplex,
                                          "Multiplexed Accumulated Sum with Views Development")
                self.add_signal(multiplex_signal, "multiplex_views")
                self.add_transition(multiplex_operation, multiplex_signal, label="thread")
            except Exception as no_view_statistics_error:
                LOGGER.debug(
                    "[{}.multiplex_2] multiplex not possible!, exited with '{}'".format(
                        self.__class__.__name__, no_view_statistics_error))
        except Exception as multiplex_exception:
            self.exception_queue.put(multiplex_exception)

    @Profiling
    @Debugger
    def rate_of_change_2(self):
        """
        method for calculating percentage change in prices

        """
        ownership_history = self.get_signal("final_ownership_history")
        price_change_operation = RateOfChange(
            ownership_history.data, "Calculate Percentage Change in Real-estate Price")
        self.add_node(price_change_operation)
        price_change = {"historikk": price_change_operation.run()}

        self.add_transition(self.get_signal("final_ownership_history"),
                            price_change_operation)

        price_change_signal = Signal(price_change, "Ownership History with Percentage Change "
                                                   "in Real-estate Price")
        self.add_signal(price_change_signal, "price_change_signal")

        self.add_transition(price_change_operation, price_change_signal)

    @Profiling
    @Tracking
    def multiplex_3(self):
        """
        second method for multiplexing signals


        """
        multiplexed_data = self.get_signal("multiplexed_data")
        price_change = self.get_signal("price_change_signal")
        multiplex_views = self.get_signal("multiplex_views")
        community_statistics = self.get_signal("processed_community_data")

        signals = [multiplexed_data, price_change, multiplex_views, community_statistics]

        multiplex_operation = Multiplex(signals,
                                        desc="Multiplex Scraped Finn Information, Ownership History"
                                             "\n with Price Change, View- and Community Statistics")
        self.add_node(multiplex_operation)
        multiplex = multiplex_operation.run()

        self.add_transition(multiplexed_data, multiplex_operation)
        self.add_transition(price_change, multiplex_operation)
        self.add_transition(multiplex_views, multiplex_operation)
        self.add_transition(community_statistics, multiplex_operation)

        multiplex_signal = Signal(multiplex, "Multiplexed Finn Information", prettify_keys=True,
                                  length=12)
        self.add_signal(multiplex_signal, "multiplex_finn_data")

        self.add_transition(multiplex_operation, multiplex_signal)
        return multiplex

    @Profiling
    @Tracking
    def output_operation(self):
        """
        final method call in process

        """
        output_operation = OutputOperation(desc="Multiplexed Finn Information")
        self.add_node(output_operation)
        self.add_transition(self.get_signal("multiplex_finn_data"), output_operation)

        output_signal = OutputSignal(self.multiplex_info_1, desc="Finn Information",
                                     prettify_keys=True, length=14)
        self.add_signal(output_signal, "output_multiplex_data")
        self.add_transition(output_operation, output_signal)
        self.print_pdf()
