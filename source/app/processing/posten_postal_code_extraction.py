# -*- coding: utf-8 -*-

"""
Process for extracting Postal Code Information

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Profiling, Tracking

from .engine import Process, InputOperation, Signal, ValidatePostalCode, PostalCodeInfoConnector, \
    OutputSignal, OutputOperation


class PostenPostalCodeExtraction(Process):
    """
    Process for extracting Norwegian Postal Code Information from Postens public
    address search

    """

    @Tracking
    def __init__(self, postal_code: str):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        postal_code        : str
                             Postal Code to be searched

        """
        self.start_process()
        super().__init__(name=self.__class__.__name__)
        Assertor.assert_data_types([postal_code], [str])
        self.input_operation({"postal_code": postal_code})
        self.validate_postal_code()
        self.postal_code_info_connector()

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
    @Tracking
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
    @Tracking
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
    @Tracking
    def postal_code_info_connector(self):
        """
        method for retrieve Norwegian Postal Code Information from Postens public address search

        """
        validated_postal_code = self.get_signal("validated_postal_code")
        postal_code_connector_operation = PostalCodeInfoConnector(
            validated_postal_code.data["postal_code"])
        self.add_node(postal_code_connector_operation)

        self.add_transition(validated_postal_code, postal_code_connector_operation)

        postal_code_info = postal_code_connector_operation.run()
        postal_code_info_signal = Signal(postal_code_info, "Postal Code Information")
        self.add_signal(postal_code_info_signal, "postal_code_info")

        self.add_transition(postal_code_connector_operation, postal_code_info_signal)

    @Profiling
    @Tracking
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
        self.print_pdf()

        return postal_code_info.data
