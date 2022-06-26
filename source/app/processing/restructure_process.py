# -*- coding: utf-8 -*-

"""
Process for restructure mortgage data against requirement from finanstilsynet

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Profiling, Tracking, Debugger

from .engine import Process, Signal, InputOperation, ValidateRestructure


class RestructureProcess(Process):
    """
    process for restructure mortgage

    """

    @Tracking
    def __init__(self, data: dict):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        data        : dict
                      information about mortgage to be restructured

        """
        self.start_process()
        super().__init__(name=__class__.__name__)
        Assertor.assert_data_types([data], [dict])
        self.input_operation({"data": data})
        self.validate_restructure()
        self.output_operation()

        self.end_process()

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
        input_operation = InputOperation("Restructure Data")
        self.add_node(input_operation)

        input_signal = Signal(data, desc="Restructure Data")
        self.add_signal(input_signal, "input_signal")

        self.add_transition(input_operation, input_signal)

    @Profiling
    @Debugger
    def validate_restructure(self):
        """
        method for validating restructure information

        """
        input_signal = self.get_signal("input_signal")
        validate_restructure_operation = ValidateRestructure(input_signal.data["data"])
        self.add_node(validate_restructure_operation)
        self.add_transition(input_signal, validate_restructure_operation)

        validate_restructure = validate_restructure_operation.run()
        validate_restructure_signal = Signal(validate_restructure,
                                             "Validated Restructure Information",
                                             prettify_keys=True, length=4)
        self.add_signal(validate_restructure_signal, "validated_restructure")

        self.add_transition(validate_restructure_operation, validate_restructure_signal)

    @Profiling
    @Debugger
    def output_operation(self):
        """
        final method call in process

        """
        self.print_pdf()
