# -*- coding: utf-8 -*-

"""
Process for analyze mortgage data against requirement from finanstilsynet

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Profiling, Tracking, Debugger

from .engine import Process, Signal, InputOperation, ValidateMortgage, OutputSignal, \
    OutputOperation, Extract, Factor, Multiplication, Multiplex, Division, Subtraction, Addition, \
    FixedStressTest, SerialStressTest, SsbConnector


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

        self.run_parallel([self.ssb_connector, self.fixed_stress_test, self.serial_stress_test,
                           self.extract_1, self.extract_2, self.extract_3, self.factor_1,
                           self.factor_2, self.factor_3])

        self.run_parallel([self.multiply_1, self.subtraction_1, self.addition_2])
        self.run_parallel([self.addition_1, self.extract_4, self.division_1])
        self.run_parallel([self.division_2, self.division_3])
        self.run_parallel([self.subtraction_2, self.subtraction_3])

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
    def ssb_connector(self):
        """
        method for getting ssb market interest rates

        """
        ssb_connector_operation = SsbConnector()
        self.add_node(ssb_connector_operation)

        ssb_connector = ssb_connector_operation.run()
        ssb_connector_signal = Signal(ssb_connector, "SSB Market Interest Rates")
        self.add_signal(ssb_connector_signal, "ssb_interest_rates")

        self.add_transition(ssb_connector_operation, ssb_connector_signal, label="thread")

    @Profiling
    @Debugger
    def fixed_stress_test(self):
        """
        method for calculate fixed stress rate

        """
        mortgage_signal = self.get_signal("validated_mortgage")
        fixed_stress_test_operation = FixedStressTest(mortgage_signal.data)
        self.add_node(fixed_stress_test_operation)
        self.add_transition(mortgage_signal, fixed_stress_test_operation, label="thread")

        fixed_stress_test = fixed_stress_test_operation.run()
        fixed_stress_test_signal = Signal(fixed_stress_test, "Fixed Stress Test")

        self.add_signal(fixed_stress_test_signal, "fixed_stress_test")
        self.add_transition(fixed_stress_test_operation,
                            fixed_stress_test_signal, label="thread")

    @Profiling
    @Debugger
    def serial_stress_test(self):
        """
        method for calculate serial stress rate

        """
        mortgage_signal = self.get_signal("validated_mortgage")
        serial_stress_test_operation = SerialStressTest(mortgage_signal.data)
        self.add_node(serial_stress_test_operation)
        self.add_transition(mortgage_signal, serial_stress_test_operation, label="thread")

        serial_stress_test = serial_stress_test_operation.run()
        serial_stress_test_signal = Signal(serial_stress_test, "Fixed Stress Test")

        self.add_signal(serial_stress_test_signal, "serial_stress_test")
        self.add_transition(serial_stress_test_operation,
                            serial_stress_test_signal, label="thread")

    @Profiling
    @Debugger
    def extract_1(self):
        """
        method for extracting gross monthly income

        """
        validated_mortgage = self.get_signal("validated_mortgage")
        total_income_extract_operation = Extract(validated_mortgage.data, "personinntekt_total_aar")
        self.add_node(total_income_extract_operation)
        self.add_transition(validated_mortgage, total_income_extract_operation, label="thread")

        total_income_extract = total_income_extract_operation.run()
        total_income_extract['arsinntekt_aar'] = total_income_extract.pop('personinntekt_total_aar')

        total_income_extract_signal = Signal(total_income_extract, "Total Monthly Gross Income")

        self.add_signal(total_income_extract_signal, "arsinntekt_aar")
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

        equity_extract_signal = Signal(equity_extract, "Total Equity")

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
        factor_operation = Factor("5", "Mortgage Limit")
        self.add_node(factor_operation)

        factor = factor_operation.run()
        factor_signal = Signal(factor, "Mortgage Limit")

        self.add_signal(factor_signal, "mortgage_limit")
        self.add_transition(factor_operation, factor_signal, label="thread")

    @Profiling
    @Debugger
    def factor_2(self):
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
        method for calculating total mortgage limit

        """

        mortgage_limit_operation = Multiplication(
            {'belaning': self.get_signal("arsinntekt_aar").data['arsinntekt_aar']},
            self.get_signal("mortgage_limit").data, "Calculate Total Mortgage Limit")
        self.add_node(mortgage_limit_operation)

        self.add_transition(self.get_signal("arsinntekt_aar"), mortgage_limit_operation,
                            label="thread")
        self.add_transition(self.get_signal("mortgage_limit"), mortgage_limit_operation,
                            label="thread")

        mortgage_limit = mortgage_limit_operation.run(money=True)

        mortgage_limit_signal = Signal(mortgage_limit, "Total Mortgage Limit", prettify_keys=True,
                                       length=10)

        self.add_signal(mortgage_limit_signal, "belaning")
        self.add_transition(mortgage_limit_operation, mortgage_limit_signal, label="thread")

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
                            label="thread")
        self.add_transition(self.get_signal("belaning"), financing_frame_operation,
                            label="thread")

        financing_frame = financing_frame_operation.run(money=True)
        financing_frame_signal = Signal(financing_frame, "Calculated Total Financing Frame",
                                        prettify_keys=True, length=10)

        self.add_signal(financing_frame_signal, "total_ramme")

        self.add_transition(financing_frame_operation, financing_frame_signal, label="thread")

    @Profiling
    @Debugger
    def addition_2(self):
        """
        method for calculating required interest rates

        """

        required_interest_rates_operation = Addition(
            {"krav_stresstest_annuitet": self.get_signal("ssb_interest_rates").data[
                'markedsrente']},
            self.get_signal("mortgage_limit").data,
            "Calculate Required Stress Rate")
        self.add_node(required_interest_rates_operation)

        self.add_transition(self.get_signal("ssb_interest_rates"),
                            required_interest_rates_operation,
                            label="thread")
        self.add_transition(self.get_signal("mortgage_limit"), required_interest_rates_operation,
                            label="thread")

        required_fixed_interest_rates = required_interest_rates_operation.run(money=False,
                                                                              percent=True)
        required_serial_interest_rates = {
            'krav_stresstest_serie': required_fixed_interest_rates['krav_stresstest_annuitet']}

        fixed_required_interest_rates_signal = Signal(required_fixed_interest_rates,
                                                      "Calculated Required Fixed Stress Rate",
                                                      prettify_keys=True, length=10)
        serial_required_interest_rates_signal = Signal(required_serial_interest_rates,
                                                       "Calculated Required Serial Stress Rate",
                                                       prettify_keys=True, length=10)

        self.add_signal(fixed_required_interest_rates_signal, "required_fixed_rates")
        self.add_signal(serial_required_interest_rates_signal, "required_serial_rates")

        self.add_transition(required_interest_rates_operation, fixed_required_interest_rates_signal,
                            label="thread")
        self.add_transition(required_interest_rates_operation,
                            serial_required_interest_rates_signal,
                            label="thread")

    @Profiling
    @Debugger
    def division_1(self):
        """
        method for equity share

        """

        equity_share_operation = Division(
            {"egenkapital_andel": self.get_signal("egenkapital").data["egenkapital_2"]},
            self.get_signal("total_ramme").data, "Calculate Equity Share")
        self.add_node(equity_share_operation)

        self.add_transition(self.get_signal("egenkapital"), equity_share_operation,
                            label="thread")
        self.add_transition(self.get_signal("total_ramme"), equity_share_operation, label="thread")

        equity_share = equity_share_operation.run()
        equity_share_signal = Signal(equity_share, "Calculated Equity Share",
                                     prettify_keys=True, length=10)

        self.add_signal(equity_share_signal, "egenkapital_andel")

        self.add_transition(equity_share_operation, equity_share_signal, label="thread")

    @Profiling
    @Debugger
    def extract_4(self):
        """
        method for extracting mortgage limit

        """
        mortgage_limit = self.get_signal("belaning")
        extract_mortgage_limit_operation = Extract(mortgage_limit.data, "belaning")
        self.add_node(extract_mortgage_limit_operation)
        self.add_transition(mortgage_limit, extract_mortgage_limit_operation, label="thread")

        extract_mortgage_limit = extract_mortgage_limit_operation.run()
        extract_mortgage_limit['krav_belaning'] = extract_mortgage_limit.pop('belaning')

        extract_mortgage_signal = Signal(extract_mortgage_limit, "Required Mortgage Limit")

        self.add_signal(extract_mortgage_signal, "krav_belaning")
        self.add_transition(extract_mortgage_limit_operation, extract_mortgage_signal,
                            label="thread")

    @Profiling
    @Debugger
    def factor_3(self):
        """
        method for creating a factor

        """
        factor_operation = Factor("15", "Required Equity Share")
        self.add_node(factor_operation)

        factor = factor_operation.run()
        factor['krav_egenkapital_andel'] = factor.pop('factor')
        factor.update({'krav_egenkapital_andel': '15.0 %'})

        factor_signal = Signal(factor, "Required Equity Share")

        self.add_signal(factor_signal, "krav_egenkapital_andel")
        self.add_transition(factor_operation, factor_signal, label="thread")

    @Profiling
    @Debugger
    def subtraction_1(self):
        """
        method for calculating required mortgage share

        """

        required_mortgage_share_operation = Subtraction(
            {"krav_belaningsgrad": self.get_signal("full_financing").data['factor']},
            self.get_signal("krav_egenkapital_andel").data,
            "Calculate Required Mortgage Share")
        self.add_node(required_mortgage_share_operation)

        self.add_transition(self.get_signal("krav_egenkapital_andel"),
                            required_mortgage_share_operation, label="thread")
        self.add_transition(self.get_signal("full_financing"), required_mortgage_share_operation,
                            label="thread")

        required_mortgage_share = required_mortgage_share_operation.run(percent=True)
        required_mortgage_share_signal = Signal(required_mortgage_share,
                                                "Calculated Required Mortgage Share",
                                                prettify_keys=True, length=10)

        self.add_signal(required_mortgage_share_signal, "krav_belaningsgrad")

        self.add_transition(required_mortgage_share_operation, required_mortgage_share_signal,
                            label="thread")

    @Profiling
    @Debugger
    def subtraction_2(self):
        """
        method for calculating mortgage share

        """

        mortgage_share_operation = Subtraction(
            {"belaningsgrad": self.get_signal("full_financing").data['factor']},
            self.get_signal("egenkapital_andel").data,
            "Calculate Mortgage Share")
        self.add_node(mortgage_share_operation)

        self.add_transition(self.get_signal("egenkapital_andel"), mortgage_share_operation,
                            label="thread")
        self.add_transition(self.get_signal("full_financing"), mortgage_share_operation,
                            label="thread")

        mortgage_share = mortgage_share_operation.run(percent=True)
        mortgage_share_signal = Signal(mortgage_share, "Calculated Mortgage Share",
                                       prettify_keys=True, length=10)

        self.add_signal(mortgage_share_signal, "belaningsgrad")

        self.add_transition(mortgage_share_operation, mortgage_share_signal, label="thread")

    @Profiling
    @Debugger
    def division_2(self):
        """
        method for calculating required mortgage share

        """

        required_mortgage_share_operation = Division(
            {"krav_belaning_verdi": self.get_signal("krav_belaningsgrad").data[
                "krav_belaningsgrad"]},
            self.get_signal("full_financing").data,
            "Calculate Required Mortgage Share as Percentage")
        self.add_node(required_mortgage_share_operation)

        self.add_transition(self.get_signal("full_financing"), required_mortgage_share_operation,
                            label="thread")
        self.add_transition(self.get_signal("krav_belaningsgrad"),
                            required_mortgage_share_operation,
                            label="thread")

        required_mortgage_share = required_mortgage_share_operation.run(percent=False)
        required_mortgage_share_signal = Signal(required_mortgage_share,
                                                "Calculated Required Mortgage Share as Percentage",
                                                prettify_keys=True, length=10)

        self.add_signal(required_mortgage_share_signal, "krav_belaning_verdi")

        self.add_transition(required_mortgage_share_operation, required_mortgage_share_signal,
                            label="thread")

    @Profiling
    @Debugger
    def division_3(self):
        """
        method for calculating required total frame

        """

        required_total_frame_operation = Division(
            {"krav_total_ramme": self.get_signal("krav_belaning").data[
                "krav_belaning"]},
            self.get_signal("krav_belaning_verdi").data,
            "Calculate Required Total Financing Frame")
        self.add_node(required_total_frame_operation)

        self.add_transition(self.get_signal("krav_belaning_verdi"),
                            required_total_frame_operation,
                            label="thread")
        self.add_transition(self.get_signal("krav_belaning"),
                            required_total_frame_operation,
                            label="thread")

        required_total_frame = required_total_frame_operation.run(percent=False, money=True)

        required_total_frame_signal = Signal(required_total_frame,
                                             "Calculated Required Total Financing Frame",
                                             prettify_keys=True, length=10)

        self.add_signal(required_total_frame_signal, "krav_total_ramme")

        self.add_transition(required_total_frame_operation, required_total_frame_signal,
                            label="thread")

    @Profiling
    @Debugger
    def subtraction_3(self):
        """
        method for calculating required equity

        """

        required_equity_operation = Subtraction(
            {"krav_egenkapital": self.get_signal("krav_total_ramme").data['krav_total_ramme']},
            self.get_signal("krav_belaning").data,
            "Calculate Required Equity")
        self.add_node(required_equity_operation)

        self.add_transition(self.get_signal("krav_total_ramme"), required_equity_operation,
                            label="thread")
        self.add_transition(self.get_signal("krav_belaning"), required_equity_operation,
                            label="thread")

        required_equity = required_equity_operation.run(money=True, rnd=0)
        required_equity_signal = Signal(required_equity, "Calculated Required Equity",
                                        prettify_keys=True, length=10)

        self.add_signal(required_equity_signal, "krav_egenkapital")

        self.add_transition(required_equity_operation, required_equity_signal, label="thread")

    @Profiling
    @Debugger
    def multiplex(self):
        """
        multiplex mortgage information

        """
        fixed_stress_rate = self.get_signal("fixed_stress_test")
        serial_stress_rate = self.get_signal("serial_stress_test")
        required_fixed_rates = self.get_signal("required_fixed_rates")
        required_serial_rates = self.get_signal("required_serial_rates")
        equity = self.get_signal("egenkapital")
        net_liquidity = self.get_signal("netto_likviditet")
        yearly_income = self.get_signal("arsinntekt_aar")
        mortgage_limit = self.get_signal("belaning")
        equity_share = self.get_signal("egenkapital_andel")
        mortgage_share = self.get_signal("belaningsgrad")
        total_financing_frame = self.get_signal("total_ramme")
        required_mortgage_limit = self.get_signal("krav_belaning")
        required_equity_share = self.get_signal("krav_egenkapital_andel")
        required_mortgage_share = self.get_signal("krav_belaningsgrad")
        required_total_financing_frame = self.get_signal("krav_total_ramme")
        required_equity = self.get_signal("krav_egenkapital")

        multiplex_operation = Multiplex([fixed_stress_rate, serial_stress_rate,
                                         required_fixed_rates, required_serial_rates, equity,
                                         net_liquidity, yearly_income, mortgage_limit, equity_share,
                                         mortgage_share, total_financing_frame,
                                         required_mortgage_limit, required_equity_share,
                                         required_mortgage_share, required_total_financing_frame,
                                         required_equity], "Multiplex Mortgage Information")

        self.add_node(multiplex_operation)

        self.add_transition(fixed_stress_rate, multiplex_operation)
        self.add_transition(serial_stress_rate, multiplex_operation)
        self.add_transition(required_fixed_rates, multiplex_operation)
        self.add_transition(required_serial_rates, multiplex_operation)
        self.add_transition(equity, multiplex_operation)
        self.add_transition(net_liquidity, multiplex_operation)
        self.add_transition(yearly_income, multiplex_operation)
        self.add_transition(mortgage_limit, multiplex_operation)
        self.add_transition(equity_share, multiplex_operation)
        self.add_transition(mortgage_share, multiplex_operation)
        self.add_transition(total_financing_frame, multiplex_operation)
        self.add_transition(required_mortgage_limit, multiplex_operation)
        self.add_transition(required_equity_share, multiplex_operation)
        self.add_transition(required_mortgage_share, multiplex_operation)
        self.add_transition(required_total_financing_frame, multiplex_operation)
        self.add_transition(required_equity, multiplex_operation)

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
