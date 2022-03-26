# -*- coding: utf-8 -*-

"""
Process for validating tax form

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking, Profiling

from .engine import Process, Signal, InputOperation, ValidateTaxForm


class SkatteetatenTaxProcessing(Process):
    """
    Process for tax calculating given Skatteetaten rules

    """

    def __init__(self, tax_data: dict):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        tax_data        : dict
                          dictionary with tax information

        """
        self.start_process()
        super().__init__(name=__class__.__name__)
        self.input_operation({"data": tax_data})
        self.validate_tax_form()
        self.output_operation()
        self.end_process()

    @Profiling
    @Tracking
    def input_operation(self, data: dict):
        """
        method for retrieving information from Tax form and saving it to Tax processing object

        Parameters
        ----------
        data        : dict
                      data sent in to process

        """
        Assertor.assert_data_types([data], [dict])
        input_operation = InputOperation("Skatteetaten Tax Form Data")
        self.add_node(input_operation)

        input_signal = Signal(data, desc="Skatteetaten Tax Form Data")
        self.add_signal(input_signal, "input_signal")

        self.add_transition(input_operation, input_signal)

    @Profiling
    @Tracking
    def validate_tax_form(self):
        """
        method for validating tax_form information

        """
        input_signal = self.get_signal("input_signal")
        validate_tax_form_operation = ValidateTaxForm(input_signal.data["data"])
        self.add_node(validate_tax_form_operation)
        self.add_transition(input_signal, validate_tax_form_operation)

        tax_form = validate_tax_form_operation.run()
        populate_signal = Signal(tax_form, "Validated Tax Form Information", prettify_keys=True,
                                 length=6)
        self.add_signal(populate_signal, "validated_tax_form")

        self.add_transition(validate_tax_form_operation, populate_signal)

    @Profiling
    @Tracking
    def output_operation(self):
        """
        final method call in process

        """
        self.print_pdf()
