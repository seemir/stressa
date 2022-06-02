# -*- coding: utf-8 -*-

"""
Process for analyze mortgage data against requirement from finanstilsynet

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Profiling, Tracking, Debugger

from .engine import Process, Signal, InputOperation, ValidateMortgage, OutputSignal, OutputOperation


class MortgageAnalysisProcess(Process):
    """
    process for analyzing mortgage

    """

    @Tracking
    def __init__(self, data: dict):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        data        : dict
                      information about mortgage to be analyzed

        """
        self.start_process()
        super().__init__(name=__class__.__name__)
        Assertor.assert_data_types([data], [dict])
        self.input_operation({"data": data})
        self.validate_mortgage()

        self._mortgage = self.output_operation()

        self.end_process()

    def mortgage(self):
        """
        mortgage getter

        Returns
        -------
        out         : dict
                      active mortgage in object

        """
        return self._mortgage

    @Profiling
    @Debugger
    def input_operation(self, data: dict):
        """
        initial method in process

        Parameters
        ----------
        data        : dict
                      data sent in to processed

        """
        Assertor.assert_data_types([data], [dict])
        input_operation = InputOperation("Mortgage Data")
        self.add_node(input_operation)

        input_signal = Signal(data, desc="Mortgage Data")
        self.add_signal(input_signal, "input_signal")

        self.add_transition(input_operation, input_signal)

    @Profiling
    @Debugger
    def validate_mortgage(self):
        """
        method for validating mortgage information

        """
        input_signal = self.get_signal("input_signal")
        validate_mortgage_operation = ValidateMortgage(input_signal.data["data"])
        self.add_node(validate_mortgage_operation)
        self.add_transition(input_signal, validate_mortgage_operation)

        mortgage = validate_mortgage_operation.run()
        mortgage_signal = Signal(mortgage, "Validated Mortgage Information", prettify_keys=True,
                                 length=6)
        self.add_signal(mortgage_signal, "validated_mortgage")

        self.add_transition(validate_mortgage_operation, mortgage_signal)

    @Profiling
    @Debugger
    def output_operation(self):
        """
        final method call in process

        """
        validated_mortgage = self.get_signal("validated_mortgage")
        output_operation = OutputOperation("Validated Mortgage")
        self.add_node(output_operation)
        self.add_transition(validated_mortgage, output_operation)

        output_signal = OutputSignal(validated_mortgage.data,
                                     desc="Validated Mortgage", prettify_keys=True,
                                     length=4)
        self.add_signal(output_signal, "output_data")
        self.add_transition(output_operation, output_signal)
        self.print_pdf()

        return validated_mortgage.data
