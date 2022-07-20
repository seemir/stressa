# -*- coding: utf-8 -*-

"""
Process for restructure mortgage data against requirement from finanstilsynet

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Profiling, Tracking, Debugger

from .engine import Process, Signal, InputOperation, ValidateRestructure, FixedStressTest, \
    SerialStressTest, SsbConnector, Extract, Multiplication, Factor, Subtraction, Division, \
    Addition, FixedPayment, Multiplex, OutputOperation, OutputSignal, Converter, \
    GenerateFixedPaymentPlan, GenerateSeriesPaymentPlan


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

        self.run_parallel([self.validate_restructure, self.factor_1, self.factor_2])

        self.run_parallel([self.extract_1, self.fixed_stress_test, self.extract_2, self.extract_3,
                           self.extract_4, self.extract_5, self.factor_3, self.extract_6,
                           self.extract_7, self.serial_stress_test, self.subtraction_1])

        self.run_parallel([self.ssb_connector, self.fixed_mortgage_payment_plan,
                           self.series_mortgage_payment_plan])

        self.run_parallel([self.addition_1, self.multiply_1, self.addition_2, self.division_1])
        self.run_parallel([self.division_2, self.fixed_payment, self.division_3])
        self.run_parallel([self.subtraction_2, self.subtraction_3, self.converter_1,
                           self.converter_2])

        self.multiplex()

        self._restructure = self.output_operation()

        self.end_process()

    def restructure(self):
        """
        restructure getter

        Returns
        -------
        out         : Restructure
                      active mortgage in object

        """
        return self._restructure

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
        restructure_signal = self.get_signal("validated_restructure")
        fixed_stress_test_operation = FixedStressTest(restructure_signal.data)
        self.add_node(fixed_stress_test_operation)
        self.add_transition(restructure_signal, fixed_stress_test_operation, label="thread")

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
        restructure_signal = self.get_signal("validated_restructure")
        serial_stress_test_operation = SerialStressTest(restructure_signal.data)
        self.add_node(serial_stress_test_operation)
        self.add_transition(restructure_signal, serial_stress_test_operation, label="thread")

        serial_stress_test = serial_stress_test_operation.run()
        serial_stress_test_signal = Signal(serial_stress_test, "Fixed Stress Test")

        self.add_signal(serial_stress_test_signal, "serial_stress_test")
        self.add_transition(serial_stress_test_operation,
                            serial_stress_test_signal, label="thread")

    @Profiling
    @Debugger
    def extract_1(self):
        """
        method for extracting belaning

        """
        validated_restructure = self.get_signal("validated_restructure")
        mortgage_amount_operation = Extract(validated_restructure.data, "belaning")
        self.add_node(mortgage_amount_operation)
        self.add_transition(validated_restructure, mortgage_amount_operation, label="thread")

        mortgage_amount_extract = mortgage_amount_operation.run()
        mortgage_amount_extract_signal = Signal(mortgage_amount_extract,
                                                "Total Mortgage Amount")

        self.add_signal(mortgage_amount_extract_signal, "belaning")
        self.add_transition(mortgage_amount_operation, mortgage_amount_extract_signal,
                            label="thread")

    @Profiling
    @Debugger
    def extract_2(self):
        """
        method for extracting equity

        """
        validated_restructure = self.get_signal("validated_restructure")
        equity_extract_operation = Extract(validated_restructure.data, "egenkapital")
        self.add_node(equity_extract_operation)
        self.add_transition(validated_restructure, equity_extract_operation, label="thread")

        equity_extract = equity_extract_operation.run()
        equity_extract['egenkapital_2'] = equity_extract.pop('egenkapital')

        equity_extract_signal = Signal(equity_extract, "Total Equity")

        self.add_signal(equity_extract_signal, "egenkapital")
        self.add_transition(equity_extract_operation, equity_extract_signal, label="thread")

    @Profiling
    @Debugger
    def extract_3(self):
        """
        method for extracting interval

        """
        validated_restructure = self.get_signal("validated_restructure")
        interval_extract_operation = Extract(validated_restructure.data, "intervall")
        self.add_node(interval_extract_operation)
        self.add_transition(validated_restructure, interval_extract_operation, label="thread")

        interval_extract = interval_extract_operation.run()
        interval_extract_signal = Signal(interval_extract, "Interval for Mortgage")

        self.add_signal(interval_extract_signal, "interval")
        self.add_transition(interval_extract_operation, interval_extract_signal, label="thread")

    @Profiling
    @Debugger
    def extract_4(self):
        """
        method for extracting period

        """
        validated_restructure = self.get_signal("validated_restructure")
        period_extract_operation = Extract(validated_restructure.data, "laneperiode")
        self.add_node(period_extract_operation)
        self.add_transition(validated_restructure, period_extract_operation, label="thread")

        period_extract = period_extract_operation.run()
        period_extract_signal = Signal(period_extract, "Period for Mortgage")

        self.add_signal(period_extract_signal, "period")
        self.add_transition(period_extract_operation, period_extract_signal, label="thread")

    @Profiling
    @Debugger
    def extract_5(self):
        """
        method for extracting gross monthly income

        """
        validated_restructure = self.get_signal("validated_restructure")
        total_income_extract_operation = Extract(validated_restructure.data,
                                                 "personinntekt_total_aar")
        self.add_node(total_income_extract_operation)
        self.add_transition(validated_restructure, total_income_extract_operation, label="thread")

        total_income_extract = total_income_extract_operation.run()
        total_income_extract['arsinntekt_aar'] = total_income_extract.pop('personinntekt_total_aar')

        total_income_extract_signal = Signal(total_income_extract, "Total Monthly Gross Income")

        self.add_signal(total_income_extract_signal, "arsinntekt_aar")
        self.add_transition(total_income_extract_operation, total_income_extract_signal,
                            label="thread")

    @Profiling
    @Debugger
    def extract_6(self):
        """
        method for extracting interval

        """
        validated_restructure = self.get_signal("validated_restructure")
        start_date_extract_operation = Extract(validated_restructure.data, "startdato")
        self.add_node(start_date_extract_operation)
        self.add_transition(validated_restructure, start_date_extract_operation, label="thread")

        start_date_extract = start_date_extract_operation.run()
        start_date_extract_signal = Signal(start_date_extract, "Start Date for Mortgage")

        self.add_signal(start_date_extract_signal, "start_date")
        self.add_transition(start_date_extract_operation, start_date_extract_signal, label="thread")

    @Profiling
    @Debugger
    def extract_7(self):
        """
        method for extracting net liquidity

        """
        validated_restructure = self.get_signal("validated_restructure")
        net_liquidity_extract_operation = Extract(validated_restructure.data, "netto_likviditet")
        self.add_node(net_liquidity_extract_operation)
        self.add_transition(validated_restructure, net_liquidity_extract_operation, label="thread")

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
    def factor_3(self):
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
    def multiply_1(self):
        """
        method for calculating total mortgage limit

        """

        mortgage_limit_operation = Multiplication(
            {'krav_belaning': self.get_signal("arsinntekt_aar").data['arsinntekt_aar']},
            self.get_signal("mortgage_limit").data, "Calculate Total Mortgage Limit")
        self.add_node(mortgage_limit_operation)

        self.add_transition(self.get_signal("arsinntekt_aar"), mortgage_limit_operation,
                            label="thread")
        self.add_transition(self.get_signal("mortgage_limit"), mortgage_limit_operation,
                            label="thread")

        mortgage_limit = mortgage_limit_operation.run(money=True)

        mortgage_limit_signal = Signal(mortgage_limit, "Total Mortgage Limit", prettify_keys=True,
                                       length=10)

        self.add_signal(mortgage_limit_signal, "krav_belaning")
        self.add_transition(mortgage_limit_operation, mortgage_limit_signal, label="thread")

    @Profiling
    @Debugger
    def division_1(self):
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
    def division_2(self):
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
    def fixed_payment(self):
        """
        method for calculating fixed payment

        """
        interest = self.get_signal("required_fixed_rates")
        period = self.get_signal("period")
        interval = self.get_signal("interval")
        amount = self.get_signal("krav_belaning")

        fixed_payment_operation = FixedPayment(interest.data['krav_stresstest_annuitet'],
                                               period.data['laneperiode'],
                                               interval.data['intervall'],
                                               amount.data['krav_belaning'])
        self.add_node(fixed_payment_operation)

        self.add_transition(interest, fixed_payment_operation, label="thread")
        self.add_transition(period, fixed_payment_operation, label="thread")
        self.add_transition(interval, fixed_payment_operation, label="thread")
        self.add_transition(amount, fixed_payment_operation, label="thread")

        fixed_payment = fixed_payment_operation.run()

        fixed_payment_signal = Signal(fixed_payment, "Calculated Fixed Amount")
        self.add_signal(fixed_payment_signal, "fixed_amount")
        self.add_transition(fixed_payment_operation, fixed_payment_signal, label="thread")

    @Profiling
    @Debugger
    def converter_1(self):
        """
        method for converting net liquidity to monthly values

        """
        interval = self.get_signal("interval")
        fixed_amount = self.get_signal("fixed_amount")

        converter_operation = Converter(fixed_amount.data, interval.data['intervall'], 'Månedlig')
        self.add_node(converter_operation)

        self.add_transition(interval, converter_operation, label="thread")
        self.add_transition(fixed_amount, converter_operation, label="thread")

        converter = converter_operation.run()

        converter_signal = Signal(converter, "Calculated Monthly Fixed Amount")
        self.add_signal(converter_signal, "fixed_amount_monthly")
        self.add_transition(converter_operation, converter_signal, label="thread")

    @Profiling
    @Debugger
    def converter_2(self):
        """
        method for converting net liquidity to plan values

        """
        interval = self.get_signal("interval")
        net_liquidity = self.get_signal("netto_likviditet")

        print("du er her: " + str(interval.data))
        print("du er her: " + str(net_liquidity.data))

        net_liquidity_converter_operation = Converter(net_liquidity.data, 'Månedlig',
                                                      interval.data['intervall'])
        self.add_node(net_liquidity_converter_operation)
        self.add_transition(interval, net_liquidity_converter_operation, label="thread")
        self.add_transition(net_liquidity, net_liquidity_converter_operation, label="thread")

        net_liquidity_fixed = net_liquidity_converter_operation.run()
        net_liquidity_fixed['netto_likviditet_plan_annuitet'] = net_liquidity_fixed.pop(
            'netto_likviditet_2')

        net_liquidity_fixed_signal = Signal(net_liquidity_fixed,
                                            "Converted Fixed Net Liquidity Plan")
        self.add_signal(net_liquidity_fixed_signal, "net_liquidity_plan_fixed")
        self.add_transition(net_liquidity_converter_operation, net_liquidity_fixed_signal,
                            label="thread")

        net_liquidity_fixed_mnd = {"netto_likviditet_mnd_annuitet":
                                       net_liquidity.data['netto_likviditet_2']}
        net_liquidity_fixed_mnd_signal = Signal(net_liquidity_fixed_mnd,
                                                "Monthly Fixed Net Liquidity Plan")
        self.add_signal(net_liquidity_fixed_mnd_signal, "net_liquidity_mnd_fixed")
        self.add_transition(net_liquidity_converter_operation, net_liquidity_fixed_mnd_signal,
                            label="thread")

        net_liquidity_series = {"netto_likviditet_plan_serie":
                                    self.get_signal('net_liquidity_plan_fixed').data[
                                        'netto_likviditet_plan_annuitet']}
        net_liquidity_series_signal = Signal(net_liquidity_series,
                                             "Converted Series Net Liquidity Plan")
        self.add_signal(net_liquidity_series_signal, "net_liquidity_plan_series")
        self.add_transition(net_liquidity_converter_operation, net_liquidity_series_signal,
                            label="thread")

        net_liquidity_series_mnd = {"netto_likviditet_mnd_serie":
                                        net_liquidity.data['netto_likviditet_2']}
        net_liquidity_series_mnd_signal = Signal(net_liquidity_series_mnd,
                                                 "Monthly Series Net Liquidity Plan")
        self.add_signal(net_liquidity_series_mnd_signal, "net_liquidity_mnd_series")
        self.add_transition(net_liquidity_converter_operation, net_liquidity_series_mnd_signal,
                            label="thread")

    @Profiling
    @Debugger
    def fixed_mortgage_payment_plan(self):
        """
        method for generating fixed mortgage plan

        """
        interest = self.get_signal("fixed_stress_test")
        period = self.get_signal("period")
        interval = self.get_signal("interval")
        amount = self.get_signal("belaning")
        start_date = self.get_signal("start_date")

        fixed_payment_plan_operation = GenerateFixedPaymentPlan(
            interest.data['stresstest_annuitet'],
            period.data['laneperiode'],
            interval.data['intervall'],
            amount.data['belaning'],
            start_date.data['startdato'])

        self.add_node(fixed_payment_plan_operation)

        self.add_transition(interest, fixed_payment_plan_operation, label="thread")
        self.add_transition(period, fixed_payment_plan_operation, label="thread")
        self.add_transition(interval, fixed_payment_plan_operation, label="thread")
        self.add_transition(amount, fixed_payment_plan_operation, label="thread")
        self.add_transition(start_date, fixed_payment_plan_operation, label="thread")

        fixed_payment_plan = fixed_payment_plan_operation.run()

        fixed_payment_plan_signal = Signal(fixed_payment_plan,
                                           "Generate Fixed Mortgage\n Payment Plan",
                                           prettify_keys=True, length=4)
        self.add_signal(fixed_payment_plan_signal, "fixed_payment_plan")
        self.add_transition(fixed_payment_plan_operation, fixed_payment_plan_signal, label="thread")

    @Profiling
    @Debugger
    def series_mortgage_payment_plan(self):
        """
        method for generating series mortgage plan

        """
        interest = self.get_signal("serial_stress_test")
        period = self.get_signal("period")
        interval = self.get_signal("interval")
        amount = self.get_signal("belaning")
        start_date = self.get_signal("start_date")

        series_payment_plan_operation = GenerateSeriesPaymentPlan(
            interest.data['stresstest_serie'],
            period.data['laneperiode'],
            interval.data['intervall'],
            amount.data['belaning'],
            start_date.data['startdato'])

        self.add_node(series_payment_plan_operation)

        self.add_transition(interest, series_payment_plan_operation, label="thread")
        self.add_transition(period, series_payment_plan_operation, label="thread")
        self.add_transition(interval, series_payment_plan_operation, label="thread")
        self.add_transition(amount, series_payment_plan_operation, label="thread")
        self.add_transition(start_date, series_payment_plan_operation, label="thread")

        series_payment_plan = series_payment_plan_operation.run()

        series_payment_plan_signal = Signal(series_payment_plan,
                                            "Generate Series Mortgage\n Payment Plan",
                                            prettify_keys=True, length=4)
        self.add_signal(series_payment_plan_signal, "series_payment_plan")
        self.add_transition(series_payment_plan_operation, series_payment_plan_signal,
                            label="thread")

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
        fixed_amount = self.get_signal("fixed_amount_monthly")
        fixed_payment_plan = self.get_signal("fixed_payment_plan")
        series_payment_plan = self.get_signal("series_payment_plan")
        net_liquidity_plan_fixed = self.get_signal("net_liquidity_plan_fixed")
        net_liquidity_mnd_fixed = self.get_signal("net_liquidity_mnd_fixed")
        net_liquidity_plan_series = self.get_signal("net_liquidity_plan_series")
        net_liquidity_mnd_series = self.get_signal("net_liquidity_mnd_series")

        multiplex_operation = Multiplex([fixed_stress_rate, serial_stress_rate,
                                         required_fixed_rates, required_serial_rates, equity,
                                         net_liquidity, yearly_income, mortgage_limit, equity_share,
                                         mortgage_share, total_financing_frame,
                                         required_mortgage_limit, required_equity_share,
                                         required_mortgage_share, required_total_financing_frame,
                                         required_equity, fixed_amount, fixed_payment_plan,
                                         series_payment_plan, net_liquidity_plan_fixed,
                                         net_liquidity_mnd_fixed, net_liquidity_plan_series,
                                         net_liquidity_mnd_series],
                                        "Multiplex Restructured Mortgage Information")

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
        self.add_transition(fixed_amount, multiplex_operation)
        self.add_transition(fixed_payment_plan, multiplex_operation)
        self.add_transition(series_payment_plan, multiplex_operation)
        self.add_transition(net_liquidity_plan_fixed, multiplex_operation)
        self.add_transition(net_liquidity_mnd_fixed, multiplex_operation)
        self.add_transition(net_liquidity_plan_series, multiplex_operation)
        self.add_transition(net_liquidity_mnd_series, multiplex_operation)

        multiplex = multiplex_operation.run()
        multiplex_signal = Signal(multiplex, "Multiplexed Restructure Mortgage Information",
                                  prettify_keys=True, length=4)
        self.add_signal(multiplex_signal, "multiplex_restructure_info")
        self.add_transition(multiplex_operation, multiplex_signal)

    @Profiling
    @Debugger
    def output_operation(self):
        """
        final method call in process

        """
        restructure_information = self.get_signal("multiplex_restructure_info")
        output_operation = OutputOperation("Multiplexed Restructure Information")
        self.add_node(output_operation)
        self.add_transition(restructure_information, output_operation)

        output_signal = OutputSignal(restructure_information.data,
                                     desc="Multiplexed Restructure Information", prettify_keys=True,
                                     length=4)
        self.add_signal(output_signal, "output_data")
        self.add_transition(output_operation, output_signal)
        self.print_pdf()

        return restructure_information.data
