# -*- coding: utf-8 -*-

"""
Process for analyze mortgage data against requirement from finanstilsynet

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Profiling, Tracking, Debugger

from .engine import Process, Signal, InputOperation, ValidateMortgage, OutputSignal, \
    OutputOperation, Extract, Factor, Multiply, Multiplex


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

        self.run_parallel([self.extract_1, self.extract_2, self.extract_3])
        self.run_parallel([self.factor_1, self.factor_2])
        self.multiply_1()
        self.multiply_2()
        self.multiplex()

        self._mortgage = self.output_operation()

        self.end_process()

    def mortgage(self):
        """
        mortgage getter

        Returns
        -------
        out         : Mortgage
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
                                 length=4)
        self.add_signal(mortgage_signal, "validated_mortgage")

        self.add_transition(validate_mortgage_operation, mortgage_signal)

    @Profiling
    @Debugger
    def extract_1(self):
        """
        method for extracting gross monthly income

        """
        validated_mortgage = self.get_signal("validated_mortgage")
        total_income_extract_operation = Extract(validated_mortgage.data, "brutto_inntekt_total")
        self.add_node(total_income_extract_operation)
        self.add_transition(validated_mortgage, total_income_extract_operation, label="thread")

        total_income_extract = total_income_extract_operation.run()
        total_income_extract_signal = Signal(total_income_extract, "Total Monthly Gross Income")

        self.add_signal(total_income_extract_signal, "brutto_inntekt_total")
        self.add_transition(total_income_extract_operation, total_income_extract_signal,
                            label="thread")

    @Profiling
    @Debugger
    def extract_2(self):
        """
        method for extracting equity

        """
        validated_mortgage = self.get_signal("validated_mortgage")
        equity_extract_operation = Extract(validated_mortgage.data, "egenkapital")
        self.add_node(equity_extract_operation)
        self.add_transition(validated_mortgage, equity_extract_operation, label="thread")

        equity_extract = equity_extract_operation.run()
        equity_extract_signal = Signal(equity_extract, "Total Downpayment / Equity")

        self.add_signal(equity_extract_signal, "egenkapital")
        self.add_transition(equity_extract_operation, equity_extract_signal, label="thread")

    @Profiling
    @Debugger
    def extract_3(self):
        """
        method for extracting net liquidity

        """
        validated_mortgage = self.get_signal("validated_mortgage")
        net_liquidity_extract_operation = Extract(validated_mortgage.data, "netto_likviditet")
        self.add_node(net_liquidity_extract_operation)
        self.add_transition(validated_mortgage, net_liquidity_extract_operation, label="thread")

        net_liquidity_extract = net_liquidity_extract_operation.run()
        net_liquidity_extract_signal = Signal(net_liquidity_extract, "Total Monthly Net Liquidity")

        self.add_signal(net_liquidity_extract_signal, "netto_likviditet")
        self.add_transition(net_liquidity_extract_operation, net_liquidity_extract_signal,
                            label="thread")

    @Profiling
    @Debugger
    def factor_1(self):
        """
        method for creating a factor

        """
        factor_operation = Factor("12", "Monthly factor conversion")
        self.add_node(factor_operation)

        factor = factor_operation.run()
        factor_signal = Signal(factor, "Monthly factor")

        self.add_signal(factor_signal, "monthly_factor")
        self.add_transition(factor_operation, factor_signal, label="thread")

    @Profiling
    @Debugger
    def factor_2(self):
        """
        method for creating a factor

        """
        factor_operation = Factor("5", "Mortgage Limit")
        self.add_node(factor_operation)

        factor = factor_operation.run()
        factor_signal = Signal(factor, "Mortgage Limit")

        self.add_signal(factor_signal, "mortgage_limit")
        self.add_transition(factor_operation, factor_signal, label="thread")

    @Profiling
    @Debugger
    def multiply_1(self):
        """
        method for calculating yearly income

        """

        monthly_income_operation = Multiply(
            {'arsinntekt': self.get_signal("brutto_inntekt_total").data['brutto_inntekt_total']},
            self.get_signal("monthly_factor").data,
            "Calculate Total Yearly Income")
        self.add_node(monthly_income_operation)

        self.add_transition(self.get_signal("brutto_inntekt_total"), monthly_income_operation)
        self.add_transition(self.get_signal("monthly_factor"), monthly_income_operation)

        arsinntekt = monthly_income_operation.run(money=True, rnd=0)

        arsinntekt_signal = Signal(arsinntekt, "Total Yearly Income", prettify_keys=True, length=10)

        self.add_signal(arsinntekt_signal, "arsinntekt")
        self.add_transition(monthly_income_operation, arsinntekt_signal)

    @Profiling
    @Debugger
    def multiply_2(self):
        """
        method for calculating total mortgage limit

        """

        mortgage_limit_operation = Multiply(
            {'belaning': self.get_signal("arsinntekt").data['arsinntekt']},
            self.get_signal("mortgage_limit").data, "Calculate Total Mortgage Limit")
        self.add_node(mortgage_limit_operation)

        self.add_transition(self.get_signal("arsinntekt"), mortgage_limit_operation)
        self.add_transition(self.get_signal("mortgage_limit"), mortgage_limit_operation)

        mortgage_limit = mortgage_limit_operation.run(money=True, rnd=0)

        mortgage_limit_signal = Signal(mortgage_limit, "Total Mortgage Limit", prettify_keys=True,
                                       length=10)

        self.add_signal(mortgage_limit_signal, "belaning")
        self.add_transition(mortgage_limit_operation, mortgage_limit_signal)

    @Profiling
    @Debugger
    def multiplex(self):
        """
        multiplex mortgage information

        """
        equity = self.get_signal("egenkapital")
        net_liquidity = self.get_signal("netto_likviditet")
        yearly_income = self.get_signal("arsinntekt")
        mortgage_limit = self.get_signal("belaning")

        multiplex_operation = Multiplex([equity, net_liquidity, yearly_income, mortgage_limit],
                                        "Multiplex Mortgage Information")

        self.add_node(multiplex_operation)
        self.add_transition(equity, multiplex_operation)
        self.add_transition(net_liquidity, multiplex_operation)
        self.add_transition(yearly_income, multiplex_operation)
        self.add_transition(mortgage_limit, multiplex_operation)

        multiplex = multiplex_operation.run()
        multiplex_signal = Signal(multiplex, "Multiplexed Mortgage Information", prettify_keys=True,
                                  length=4)
        self.add_signal(multiplex_signal, "multiplex_mortgage_info")
        self.add_transition(multiplex_operation, multiplex_signal)

    @Profiling
    @Debugger
    def output_operation(self):
        """
        final method call in process

        """
        mortgage_information = self.get_signal("multiplex_mortgage_info")
        output_operation = OutputOperation("Multiplexed Mortgage Information")
        self.add_node(output_operation)
        self.add_transition(mortgage_information, output_operation)

        output_signal = OutputSignal(mortgage_information.data,
                                     desc="Multiplexed Mortgage Information", prettify_keys=True,
                                     length=4)
        self.add_signal(output_signal, "output_data")
        self.add_transition(output_operation, output_signal)
        self.print_pdf()

        return mortgage_information.data
