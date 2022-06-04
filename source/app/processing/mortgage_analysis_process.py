# -*- coding: utf-8 -*-

"""
Process for analyze mortgage data against requirement from finanstilsynet

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Profiling, Tracking, Debugger

from .engine import Process, Signal, InputOperation, ValidateMortgage, OutputSignal, \
    OutputOperation, Extract, Factor, Multiplication, Multiplex, Division, Subtraction, Addition


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
        self.run_parallel([self.factor_1, self.factor_2, self.factor_3, self.factor_4])
        self.multiply_1()
        self.multiply_2()
        self.divide_1()
        self.subtraction_1()
        self.addition_1()
        self.extract_4()
        self.multiply_3()

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
        total_income_extract_operation = Extract(validated_mortgage.data, "personinntekt_total")
        self.add_node(total_income_extract_operation)
        self.add_transition(validated_mortgage, total_income_extract_operation, label="thread")

        total_income_extract = total_income_extract_operation.run()
        total_income_extract_signal = Signal(total_income_extract, "Total Monthly Gross Income")

        self.add_signal(total_income_extract_signal, "personinntekt_total")
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
        equity_extract['egenkapital_2'] = equity_extract.pop('egenkapital')

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
        net_liquidity_extract['netto_likviditet_2'] = net_liquidity_extract.pop('netto_likviditet')
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
    def factor_3(self):
        """
        method for creating a factor

        """
        factor_operation = Factor("100", "Full Financing")
        self.add_node(factor_operation)

        factor = factor_operation.run()
        factor_signal = Signal(factor, "Full Financing")

        self.add_signal(factor_signal, "full_financing")
        self.add_transition(factor_operation, factor_signal, label="thread")

    @Profiling
    @Debugger
    def multiply_1(self):
        """
        method for calculating yearly income

        """

        monthly_income_operation = Multiplication(
            {'arsinntekt': self.get_signal("personinntekt_total").data['personinntekt_total']},
            self.get_signal("monthly_factor").data,
            "Calculate Total Yearly Income")
        self.add_node(monthly_income_operation)

        self.add_transition(self.get_signal("personinntekt_total"), monthly_income_operation,
                            label="source")
        self.add_transition(self.get_signal("monthly_factor"), monthly_income_operation,
                            label="factor")

        arsinntekt = monthly_income_operation.run(money=True)

        arsinntekt_signal = Signal(arsinntekt, "Total Yearly Income", prettify_keys=True, length=10)

        self.add_signal(arsinntekt_signal, "arsinntekt")
        self.add_transition(monthly_income_operation, arsinntekt_signal)

    @Profiling
    @Debugger
    def multiply_2(self):
        """
        method for calculating total mortgage limit

        """

        mortgage_limit_operation = Multiplication(
            {'belaning': self.get_signal("arsinntekt").data['arsinntekt']},
            self.get_signal("mortgage_limit").data, "Calculate Total Mortgage Limit")
        self.add_node(mortgage_limit_operation)

        self.add_transition(self.get_signal("arsinntekt"), mortgage_limit_operation, label="source")
        self.add_transition(self.get_signal("mortgage_limit"), mortgage_limit_operation,
                            label="factor")

        mortgage_limit = mortgage_limit_operation.run(money=True)

        mortgage_limit_signal = Signal(mortgage_limit, "Total Mortgage Limit", prettify_keys=True,
                                       length=10)

        self.add_signal(mortgage_limit_signal, "belaning")
        self.add_transition(mortgage_limit_operation, mortgage_limit_signal)

    @Profiling
    @Debugger
    def divide_1(self):
        """
        method for equity share

        """

        equity_share_operation = Division(
            {"egenkapital_andel": self.get_signal("egenkapital").data["egenkapital_2"]},
            self.get_signal("belaning").data, "Calculate Equity Share")
        self.add_node(equity_share_operation)

        self.add_transition(self.get_signal("egenkapital"), equity_share_operation,
                            label="quantity")
        self.add_transition(self.get_signal("belaning"), equity_share_operation, label="divisor")

        equity_share = equity_share_operation.run()
        equity_share_signal = Signal(equity_share, "Calculated Equity Share",
                                     prettify_keys=True, length=10)

        self.add_signal(equity_share_signal, "egenkapital_andel")

        self.add_transition(equity_share_operation, equity_share_signal)

    @Profiling
    @Debugger
    def subtraction_1(self):
        """
        method for calculating mortgage share

        """

        mortgage_share_operation = Subtraction(
            {"belaningsgrad": self.get_signal("full_financing").data['factor']},
            self.get_signal("egenkapital_andel").data,
            "Calculate Mortgage Share")
        self.add_node(mortgage_share_operation)

        self.add_transition(self.get_signal("egenkapital_andel"), mortgage_share_operation,
                            label="factor")
        self.add_transition(self.get_signal("full_financing"), mortgage_share_operation,
                            label="source")

        mortgage_share = mortgage_share_operation.run(percent=True)
        mortgage_share_signal = Signal(mortgage_share, "Calculated Mortgage Share",
                                       prettify_keys=True, length=10)

        self.add_signal(mortgage_share_signal, "belaningsgrad")

        self.add_transition(mortgage_share_operation, mortgage_share_signal)

    @Profiling
    @Debugger
    def addition_1(self):
        """
        method for calculating total financing frame

        """

        financing_frame_operation = Addition(
            {"total_ramme": self.get_signal("belaning").data['belaning']},
            self.get_signal("egenkapital").data,
            "Calculate Total Financing Frame")
        self.add_node(financing_frame_operation)

        self.add_transition(self.get_signal("egenkapital"), financing_frame_operation,
                            label="factor")
        self.add_transition(self.get_signal("belaning"), financing_frame_operation,
                            label="source")

        financing_frame = financing_frame_operation.run(money=True)
        financing_frame_signal = Signal(financing_frame, "Calculated Total Financing Frame",
                                        prettify_keys=True, length=10)

        self.add_signal(financing_frame_signal, "total_ramme")

        self.add_transition(financing_frame_operation, financing_frame_signal)

    @Profiling
    @Debugger
    def extract_4(self):
        """
        method for extracting mortgage limit

        """
        mortgage_limit = self.get_signal("belaning")
        extract_mortgage_limit_operation = Extract(mortgage_limit.data, "belaning")
        self.add_node(extract_mortgage_limit_operation)
        self.add_transition(mortgage_limit, extract_mortgage_limit_operation)

        extract_mortgage_limit = extract_mortgage_limit_operation.run()
        extract_mortgage_limit['krav_belaning'] = extract_mortgage_limit.pop('belaning')

        extract_mortgage_signal = Signal(extract_mortgage_limit, "Required Mortgage Limit")

        self.add_signal(extract_mortgage_signal, "krav_belaning")
        self.add_transition(extract_mortgage_limit_operation, extract_mortgage_signal)

    @Profiling
    @Debugger
    def factor_4(self):
        """
        method for creating a factor

        """
        factor_operation = Factor("0.15", "Required Equity Share")
        self.add_node(factor_operation)

        factor = factor_operation.run()
        factor['krav_egenkapital_andel_verdi'] = factor.pop('factor')

        factor_signal = Signal(factor, "Required Equity Share")

        self.add_signal(factor_signal, "krav_egenkapital_andel_verdi")
        self.add_transition(factor_operation, factor_signal, label="thread")

    @Profiling
    @Debugger
    def multiply_3(self):
        """
        method for calculating required equity percent

        """

        equity_percent_operation = Multiplication(
            {'krav_egenkapital_andel': self.get_signal("krav_egenkapital_andel_verdi").data[
                'krav_egenkapital_andel_verdi']},
            self.get_signal("full_financing").data, "Calculate Required Equity Share")
        self.add_node(equity_percent_operation)

        self.add_transition(self.get_signal("krav_egenkapital_andel_verdi"),
                            equity_percent_operation, label="source")
        self.add_transition(self.get_signal("full_financing"), equity_percent_operation,
                            label="factor")

        equity_percent = equity_percent_operation.run(percent=True)

        equity_percent_signal = Signal(equity_percent, "Calculate Required Equity Share",
                                       prettify_keys=True, length=10)

        self.add_signal(equity_percent_signal, "krav_egenkapital_andel")
        self.add_transition(equity_percent_operation, equity_percent_signal)

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
        equity_share = self.get_signal("egenkapital_andel")
        mortgage_share = self.get_signal("belaningsgrad")
        total_financing_frame = self.get_signal("total_ramme")
        required_mortgage_limit = self.get_signal("krav_belaning")
        required_equity_share = self.get_signal("krav_egenkapital_andel")

        multiplex_operation = Multiplex([equity, net_liquidity, yearly_income, mortgage_limit,
                                         equity_share, mortgage_share, total_financing_frame,
                                         required_mortgage_limit, required_equity_share],
                                        "Multiplex Mortgage Information")

        self.add_node(multiplex_operation)
        self.add_transition(equity, multiplex_operation)
        self.add_transition(net_liquidity, multiplex_operation)
        self.add_transition(yearly_income, multiplex_operation)
        self.add_transition(mortgage_limit, multiplex_operation)
        self.add_transition(equity_share, multiplex_operation)
        self.add_transition(mortgage_share, multiplex_operation)
        self.add_transition(total_financing_frame, multiplex_operation)
        self.add_transition(required_mortgage_limit, multiplex_operation)
        self.add_transition(required_equity_share, multiplex_operation)

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
