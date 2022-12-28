# -*- coding: utf-8 -*-

"""
Process for parsing tax data

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking, Profiling, Debugger

from .engine import Process, Signal, InputOperation, FlattenTaxResults, OutputOperation, \
    OutputSignal


class SkatteetatenTaxParsing(Process):
    """
    Process for parsing tax data

    """

    @Tracking
    def __init__(self, tax_data: dict):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        tax_data        : dict
                          dictionary with tax data

        """
        self.start_process()
        super().__init__(name=__class__.__name__)
        self.input_operation({"data": tax_data})

        self.flatten_tax_dict()

        self._skatteetaten_reults = self.output_operation()

        self.end_process()

    @property
    def skatteetaten_results(self):
        """
        skatteetaten tax results getter

        Returns
        -------
        out         : dict
                      dictionary with tax results

        """
        return self._skatteetaten_reults

    @Profiling
    @Debugger
    def input_operation(self, data: dict):
        """
        method for parsing tax data

        Parameters
        ----------
        data        : dict
                      data sent in to process

        """
        Assertor.assert_data_types([data], [dict])
        input_operation = InputOperation("Skatteetaten Tax Data")
        self.add_node(input_operation)

        input_signal = Signal(data, desc="Skatteetaten Tax Data")
        self.add_signal(input_signal, "input_signal")

        self.add_transition(input_operation, input_signal)

    @Profiling
    @Debugger
    def flatten_tax_dict(self):
        """
        method for flattning a tax results dictionary

        """
        input_signal = self.get_signal("input_signal")
        flatten_tax_dict_operation = FlattenTaxResults(input_signal.data["data"],
                                                       "Flatten Tax Results")
        self.add_node(flatten_tax_dict_operation)
        self.add_transition(input_signal, flatten_tax_dict_operation)

        flatten_tax_dict = flatten_tax_dict_operation.run()
        flatten_tax_dict_signal = Signal(flatten_tax_dict, "Flattened Tax Results",
                                         prettify_keys=True, length=2)
        self.add_signal(flatten_tax_dict_signal, "flatten_tax_results")

        self.add_transition(flatten_tax_dict_operation, flatten_tax_dict_signal)

    @Profiling
    @Debugger
    def output_operation(self):
        """
        final method call in process

        """
        flatten_results = self.get_signal("flatten_tax_results")

        output_operation = OutputOperation("Skatteetaten Tax Results")
        self.add_node(output_operation)
        self.add_transition(flatten_results, output_operation)

        output_signal = OutputSignal(flatten_results.data,
                                     desc="Skatteetaten Tax Results", prettify_keys=True,
                                     length=2)
        self.add_signal(output_signal, "output_data")
        self.add_transition(output_operation, output_signal)
        self.print_pdf()
        return flatten_results.data
