# -*- coding: utf-8 -*-

"""
Process for extracting Postal Code Information

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Profiling

from .engine import Process, InputOperation, Signal, ValidatePostalCode, ScrapePostalCodeInfo, \
    OutputSignal, OutputOperation


class PostalCodeExtraction(Process):
    """
    Process for extracting Norwegian Postal Code Information from Postens public
    address search

    """

    def __init__(self, postal_code: str):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        postal_code        : str
                             Postal Code to be searched

        """
        super().__init__(name=self.__class__.__name__)
        self.start_process()
        Assertor.assert_data_types([postal_code], [str])
        self.input_operation({"postal_code": postal_code})
        self.validate_postal_code()
        self.scrape_postal_code_info()

        self._postal_code_info = self.output_operation()
        self.end_process()

    @property
    def postal_code_info(self):
        """
        postal_code_info getter

        Returns
        -------
        out     : dict
                  active postal_code_info

        """
        return self._postal_code_info

    @Profiling
    def input_operation(self, data: object):
        """
        initial operation in process

        Parameters
        ----------
        data             : dict
                           postal_code sent in to process

        Returns
        -------
        out              : dict
                           postal_code saved as signal

        """
        Assertor.assert_data_types([data], [dict])
        input_operation = InputOperation("Postal Code")
        self.add_node(input_operation)

        input_signal = Signal(data, desc="Postal Code")
        self.add_signal(input_signal, "input_signal")

        self.add_transition(input_operation, input_signal)

    @Profiling
    def validate_postal_code(self):
        """
        method for validating Postal Code

        """
        input_signal = self.get_signal("input_signal")
        validate_postal_code = ValidatePostalCode(input_signal.data["postal_code"])
        self.add_node(validate_postal_code)

        self.add_transition(input_signal, validate_postal_code)

        validated_postal_code = {"postal_code": validate_postal_code.run()}
        validated_postal_code_signal = Signal(validated_postal_code, "Validated Postal Code")
        self.add_signal(validated_postal_code_signal, "validated_postal_code")

        self.add_transition(validate_postal_code, validated_postal_code_signal)

    @Profiling
    def scrape_postal_code_info(self):
        """
        method for scraping Norwegian Postal Code Information from Postens public address search

        """
        validated_postal_code = self.get_signal("validated_postal_code")
        scrape_postal_code_operation = ScrapePostalCodeInfo(
            validated_postal_code.data["postal_code"])
        self.add_node(scrape_postal_code_operation)

        self.add_transition(validated_postal_code, scrape_postal_code_operation)

        postal_code_info = scrape_postal_code_operation.run()
        postal_code_info_signal = Signal(postal_code_info, "Postal Code Information")
        self.add_signal(postal_code_info_signal, "postal_code_info")

        self.add_transition(scrape_postal_code_operation, postal_code_info_signal)

    @Profiling
    def output_operation(self):
        """
        final method call in process

        """
        postal_code_info = self.get_signal("postal_code_info")
        output_operation = OutputOperation("Postal Code Information")
        self.add_node(output_operation)
        self.add_transition(postal_code_info, output_operation)

        output_signal = OutputSignal(postal_code_info.data, desc="Postal Code Information")
        self.add_signal(output_signal, "output_data")
        self.add_transition(output_operation, output_signal)
        return postal_code_info.data
