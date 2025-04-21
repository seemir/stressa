# -*- coding: utf-8 -*-

"""
Process for restructure mortgage data against requirement from finanstilsynet

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Profiling, Tracking, Debugger

from .engine import Process, Signal, InputOperation, ValidateRestructure, \
    FixedStressTest, \
    SerialStressTest, SsbConnector, Extract, Multiplication, Factor, \
    Subtraction, Division, \
    Addition, FixedPayment, Multiplex, OutputOperation, OutputSignal, Converter, \
    GenerateFixedPaymentPlan, GenerateSeriesPaymentPlan, Comparison, \
    ReadSettings


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

        self.run_parallel(
            [self.validate_restructure, self.read_settings_1, self.factor_1])

        self.run_parallel(
            [self.extract_1, self.fixed_stress_test, self.extract_2, self.extract_3, self.extract_4,
             self.extract_5, self.read_settings_2, self.extract_6, self.extract_7, self.extract_8,
             self.serial_stress_test, self.subtraction_1, self.read_settings_3])

        self.run_parallel([self.ssb_connector, self.fixed_mortgage_payment_plan,
                           self.series_mortgage_payment_plan, self.multiply_1])

        self.run_parallel([self.addition_1, self.division_1, self.comparison_1, self.addition_2])

        self.run_parallel(
            [self.division_2, self.fixed_payment, self.division_3])
        self.run_parallel(
            [self.subtraction_2, self.subtraction_3, self.converter_1, self.converter_2])

        self.run_parallel([self.extract_9, self.extract_10])

        self.division_4()
        self.converter_3()

        self.subtraction_4()

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
        validate_restructure_operation = ValidateRestructure(
            input_signal.data["data"])
        self.add_node(validate_restructure_operation)
        self.add_transition(input_signal, validate_restructure_operation)

        validate_restructure = validate_restructure_operation.run()
        validate_restructure_signal = Signal(validate_restructure,
                                             "Validated Restructure Information",
                                             prettify_keys=True, length=5)
        self.add_signal(validate_restructure_signal, "validated_restructure")

        self.add_transition(validate_restructure_operation,
                            validate_restructure_signal)

    @Profiling
    @Debugger
    def ssb_connector(self):
        """
        method for getting ssb market interest rates

        """
        ssb_connector_operation = SsbConnector()
        self.add_node(ssb_connector_operation)

        ssb_connector = ssb_connector_operation.run()
        ssb_connector_signal = Signal(ssb_connector,
                                      "SSB Market Interest Rates")
        self.add_signal(ssb_connector_signal, "ssb_interest_rates")

        self.add_transition(ssb_connector_operation, ssb_connector_signal,
                            label="thread")

    @Profiling
    @Debugger
    def fixed_stress_test(self):
        """
        method for calculate fixed stress rate

        """
        restructure_signal = self.get_signal("validated_restructure")
        fixed_stress_test_operation = FixedStressTest(restructure_signal.data)
        self.add_node(fixed_stress_test_operation)
        self.add_transition(restructure_signal, fixed_stress_test_operation,
                            label="thread")

        fixed_stress_test = fixed_stress_test_operation.run()
        fixed_stress_test_signal = Signal(fixed_stress_test,
                                          "Fixed Stress Test")

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
        self.add_transition(restructure_signal, serial_stress_test_operation,
                            label="thread")

        serial_stress_test = serial_stress_test_operation.run()
        serial_stress_test_signal = Signal(serial_stress_test,
                                           "Fixed Stress Test")

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
        mortgage_amount_operation = Extract(validated_restructure.data,
                                            "belaning")
        self.add_node(mortgage_amount_operation)
        self.add_transition(validated_restructure, mortgage_amount_operation,
                            label="thread")

        mortgage_amount_extract = mortgage_amount_operation.run()
        mortgage_amount_extract_signal = Signal(mortgage_amount_extract,
                                                "Total Mortgage Amount")

        self.add_signal(mortgage_amount_extract_signal, "belaning")
        self.add_transition(mortgage_amount_operation,
                            mortgage_amount_extract_signal,
                            label="thread")

    @Profiling
    @Debugger
    def extract_2(self):
        """
        method for extracting equity

        """
        validated_restructure = self.get_signal("validated_restructure")
        equity_extract_operation = Extract(validated_restructure.data,
                                           "egenkapital")
        self.add_node(equity_extract_operation)
        self.add_transition(validated_restructure, equity_extract_operation,
                            label="thread")

        equity_extract = equity_extract_operation.run()
        equity_extract['egenkapital_2'] = equity_extract.pop('egenkapital')

        equity_extract_signal = Signal(equity_extract, "Total Equity")

        self.add_signal(equity_extract_signal, "egenkapital")
        self.add_transition(equity_extract_operation, equity_extract_signal,
                            label="thread")

    @Profiling
    @Debugger
    def extract_3(self):
        """
        method for extracting interval

        """
        validated_restructure = self.get_signal("validated_restructure")
        interval_extract_operation = Extract(validated_restructure.data,
                                             "intervall")
        self.add_node(interval_extract_operation)
        self.add_transition(validated_restructure, interval_extract_operation,
                            label="thread")

        interval_extract = interval_extract_operation.run()
        interval_extract_signal = Signal(interval_extract,
                                         "Interval for Mortgage")

        self.add_signal(interval_extract_signal, "interval")
        self.add_transition(interval_extract_operation, interval_extract_signal,
                            label="thread")

    @Profiling
    @Debugger
    def extract_4(self):
        """
        method for extracting period

        """
        validated_restructure = self.get_signal("validated_restructure")
        period_extract_operation = Extract(validated_restructure.data,
                                           "laneperiode")
        self.add_node(period_extract_operation)
        self.add_transition(validated_restructure, period_extract_operation,
                            label="thread")

        period_extract = period_extract_operation.run()
        period_extract_signal = Signal(period_extract, "Period for Mortgage")

        self.add_signal(period_extract_signal, "period")
        self.add_transition(period_extract_operation, period_extract_signal,
                            label="thread")

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
        self.add_transition(validated_restructure,
                            total_income_extract_operation, label="thread")

        total_income_extract = total_income_extract_operation.run()
        total_income_extract['arsinntekt_aar'] = total_income_extract.pop(
            'personinntekt_total_aar')

        total_income_extract_signal = Signal(total_income_extract,
                                             "Total Monthly Gross Income")

        self.add_signal(total_income_extract_signal, "arsinntekt_aar")
        self.add_transition(total_income_extract_operation,
                            total_income_extract_signal,
                            label="thread")

    @Profiling
    @Debugger
    def extract_6(self):
        """
        method for extracting interval

        """
        validated_restructure = self.get_signal("validated_restructure")
        start_date_extract_operation = Extract(validated_restructure.data,
                                               "startdato")
        self.add_node(start_date_extract_operation)
        self.add_transition(validated_restructure, start_date_extract_operation,
                            label="thread")

        start_date_extract = start_date_extract_operation.run()
        start_date_extract_signal = Signal(start_date_extract,
                                           "Start Date for Mortgage")

        self.add_signal(start_date_extract_signal, "start_date")
        self.add_transition(start_date_extract_operation,
                            start_date_extract_signal, label="thread")

    @Profiling
    @Debugger
    def extract_7(self):
        """
        method for extracting repayment ability

        """
        validated_restructure = self.get_signal("validated_restructure")
        repayment_ability_extract_operation = Extract(validated_restructure.data,
                                                      "betjeningsevne")
        self.add_node(repayment_ability_extract_operation)
        self.add_transition(validated_restructure,
                            repayment_ability_extract_operation, label="thread")

        repayment_ability_extract = repayment_ability_extract_operation.run()
        repayment_ability_extract['betjeningsevne_2'] = repayment_ability_extract.pop(
            'betjeningsevne')
        repayment_ability_extract_signal = Signal(repayment_ability_extract,
                                                  "Total Monthly Repayment Ability")

        self.add_signal(repayment_ability_extract_signal, "betjeningsevne")
        self.add_transition(repayment_ability_extract_operation,
                            repayment_ability_extract_signal,
                            label="thread")

    @Profiling
    @Debugger
    def extract_8(self):
        """
        method for extracting nominal interest (if any)

        """
        validated_restructure = self.get_signal("validated_restructure")
        nominal_interest_extract_operation = Extract(validated_restructure.data,
                                                     "nominell_rente")
        self.add_node(nominal_interest_extract_operation)
        self.add_transition(validated_restructure,
                            nominal_interest_extract_operation,
                            label="thread")

        nominal_interest = nominal_interest_extract_operation.run()
        nominal_extract_signal = Signal(nominal_interest,
                                        "Nominal Interest Rate")

        self.add_signal(nominal_extract_signal, "nominal_interest")
        self.add_transition(nominal_interest_extract_operation,
                            nominal_extract_signal,
                            label="thread")

    @Profiling
    @Debugger
    def read_settings_1(self):
        """
        method for creating a factor

        """
        read_settings_operation = ReadSettings("egenkapital_krav")
        self.add_node(read_settings_operation)

        factor = read_settings_operation.run()
        factor['krav_egenkapital_andel'] = factor.pop('factor')

        factor_signal = Signal(factor, "Required Equity Share")

        self.add_signal(factor_signal, "krav_egenkapital_andel")
        self.add_transition(read_settings_operation, factor_signal,
                            label="thread")

    @Profiling
    @Debugger
    def factor_1(self):
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
    def read_settings_2(self):
        """
        method for creating a factor

        """
        read_settings_operation = ReadSettings("gjeldsgrad")
        self.add_node(read_settings_operation)

        factor = read_settings_operation.run()
        factor_signal = Signal(factor, "Mortgage Limit")

        self.add_signal(factor_signal, "mortgage_limit")
        self.add_transition(read_settings_operation, factor_signal,
                            label="thread")

    @Profiling
    @Debugger
    def read_settings_3(self):
        """
        method for creating a factor

        """
        read_settings_operation = ReadSettings("stresstest")
        self.add_node(read_settings_operation)

        factor = read_settings_operation.run()
        factor_signal = Signal(factor, "Stresstest Limit")

        self.add_signal(factor_signal, "stresstest_limit")
        self.add_transition(read_settings_operation, factor_signal,
                            label="thread")

    @Profiling
    @Debugger
    def subtraction_1(self):
        """
        method for calculating required mortgage share

        """

        required_mortgage_share_operation = Subtraction(
            {"krav_belaningsgrad": self.get_signal("full_financing").data[
                'factor']},
            self.get_signal("krav_egenkapital_andel").data,
            "Calculate Required Mortgage Share")
        self.add_node(required_mortgage_share_operation)

        self.add_transition(self.get_signal("krav_egenkapital_andel"),
                            required_mortgage_share_operation, label="thread")
        self.add_transition(self.get_signal("full_financing"),
                            required_mortgage_share_operation,
                            label="thread")

        required_mortgage_share = required_mortgage_share_operation.run(
            percent=True)
        required_mortgage_share_signal = Signal(required_mortgage_share,
                                                "Calculated Required Mortgage Share",
                                                prettify_keys=True, length=10)

        self.add_signal(required_mortgage_share_signal, "krav_belaningsgrad")

        self.add_transition(required_mortgage_share_operation,
                            required_mortgage_share_signal,
                            label="thread")

    @Profiling
    @Debugger
    def multiply_1(self):
        """
        method for calculating total mortgage limit

        """

        mortgage_limit_operation = Multiplication(
            {'krav_belaning_maks': self.get_signal("arsinntekt_aar").data[
                'arsinntekt_aar']},
            self.get_signal("mortgage_limit").data,
            "Calculate Total Mortgage Limit")
        self.add_node(mortgage_limit_operation)

        self.add_transition(self.get_signal("arsinntekt_aar"),
                            mortgage_limit_operation,
                            label="thread")
        self.add_transition(self.get_signal("mortgage_limit"),
                            mortgage_limit_operation,
                            label="thread")

        mortgage_limit = mortgage_limit_operation.run(money=True)

        mortgage_limit_signal = Signal(mortgage_limit, "Total Mortgage Limit",
                                       prettify_keys=True,
                                       length=10)

        self.add_signal(mortgage_limit_signal, "krav_belaning_maks")
        self.add_transition(mortgage_limit_operation, mortgage_limit_signal,
                            label="thread")

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

        self.add_transition(self.get_signal("full_financing"),
                            required_mortgage_share_operation,
                            label="thread")
        self.add_transition(self.get_signal("krav_belaningsgrad"),
                            required_mortgage_share_operation,
                            label="thread")

        required_mortgage_share = required_mortgage_share_operation.run(
            percent=False)
        required_mortgage_share_signal = Signal(required_mortgage_share,
                                                "Calculated Required Mortgage Share as Percentage",
                                                prettify_keys=True, length=10)

        self.add_signal(required_mortgage_share_signal, "krav_belaning_verdi")

        self.add_transition(required_mortgage_share_operation,
                            required_mortgage_share_signal,
                            label="thread")

    @Profiling
    @Debugger
    def comparison_1(self):
        """
        method for comparing values

        """
        applied_mortgage = self.get_signal("belaning")
        max_mortgage = self.get_signal("krav_belaning_maks")

        comparison_operation = Comparison(applied_mortgage.data,
                                          max_mortgage.data,
                                          "krav_belaning",
                                          "Comparison of Lowest Possible Mortgage Requirement")
        self.add_node(comparison_operation)

        self.add_transition(applied_mortgage, comparison_operation)
        self.add_transition(max_mortgage, comparison_operation)

        comparison = comparison_operation.run()

        comparison_signal = Signal(comparison, "Lowest Mortgage Requirement")
        self.add_signal(comparison_signal, "krav_belaning")

        self.add_transition(comparison_operation, comparison_signal)

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

        self.add_transition(self.get_signal("egenkapital"),
                            financing_frame_operation,
                            label="thread")
        self.add_transition(self.get_signal("belaning"),
                            financing_frame_operation,
                            label="thread")

        financing_frame = financing_frame_operation.run(money=True)
        financing_frame_signal = Signal(financing_frame,
                                        "Calculated Total Financing Frame",
                                        prettify_keys=True, length=10)

        self.add_signal(financing_frame_signal, "total_ramme")

        self.add_transition(financing_frame_operation, financing_frame_signal,
                            label="thread")

    @Profiling
    @Debugger
    def division_2(self):
        """
        method for equity share

        """

        equity_share_operation = Division(
            {"egenkapital_andel": self.get_signal("egenkapital").data[
                "egenkapital_2"]},
            self.get_signal("total_ramme").data, "Calculate Equity Share")
        self.add_node(equity_share_operation)

        self.add_transition(self.get_signal("egenkapital"),
                            equity_share_operation,
                            label="thread")
        self.add_transition(self.get_signal("total_ramme"),
                            equity_share_operation, label="thread")

        equity_share = equity_share_operation.run()
        equity_share_signal = Signal(equity_share, "Calculated Equity Share",
                                     prettify_keys=True, length=10)

        self.add_signal(equity_share_signal, "egenkapital_andel")

        self.add_transition(equity_share_operation, equity_share_signal,
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

        required_total_frame = required_total_frame_operation.run(percent=False,
                                                                  money=True)

        required_total_frame_signal = Signal(required_total_frame,
                                             "Calculated Required Total Financing Frame",
                                             prettify_keys=True, length=10)

        self.add_signal(required_total_frame_signal, "krav_total_ramme")

        self.add_transition(required_total_frame_operation,
                            required_total_frame_signal,
                            label="thread")

    @Profiling
    @Debugger
    def addition_2(self):
        """
        method for calculating required interest rates

        """

        required_interest_rates_operation = Addition(
            {"krav_stresstest_annuitet":
                 self.get_signal("ssb_interest_rates").data[
                     'markedsrente']},
            self.get_signal("stresstest_limit").data,
            "Calculate Required Stress Rate")
        self.add_node(required_interest_rates_operation)

        self.add_transition(self.get_signal("ssb_interest_rates"),
                            required_interest_rates_operation,
                            label="thread")
        self.add_transition(self.get_signal("stresstest_limit"),
                            required_interest_rates_operation,
                            label="thread")

        required_fixed_interest_rates = required_interest_rates_operation.run(
            money=False,
            percent=True)
        required_serial_interest_rates = {
            'krav_stresstest_serie': required_fixed_interest_rates[
                'krav_stresstest_annuitet']}

        fixed_required_interest_rates_signal = Signal(
            required_fixed_interest_rates,
            "Calculated Required Fixed Stress Rate",
            prettify_keys=True, length=10)
        serial_required_interest_rates_signal = Signal(
            required_serial_interest_rates,
            "Calculated Required Serial Stress Rate",
            prettify_keys=True, length=10)

        self.add_signal(fixed_required_interest_rates_signal,
                        "required_fixed_rates")
        self.add_signal(serial_required_interest_rates_signal,
                        "required_serial_rates")

        self.add_transition(required_interest_rates_operation,
                            fixed_required_interest_rates_signal,
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

        self.add_transition(self.get_signal("egenkapital_andel"),
                            mortgage_share_operation,
                            label="thread")
        self.add_transition(self.get_signal("full_financing"),
                            mortgage_share_operation,
                            label="thread")

        mortgage_share = mortgage_share_operation.run(percent=True)
        mortgage_share_signal = Signal(mortgage_share,
                                       "Calculated Mortgage Share",
                                       prettify_keys=True, length=10)

        self.add_signal(mortgage_share_signal, "belaningsgrad")

        self.add_transition(mortgage_share_operation, mortgage_share_signal,
                            label="thread")

    @Profiling
    @Debugger
    def subtraction_3(self):
        """
        method for calculating required equity

        """

        required_equity_operation = Subtraction(
            {"krav_egenkapital": self.get_signal("krav_total_ramme").data[
                'krav_total_ramme']},
            self.get_signal("krav_belaning").data,
            "Calculate Required Equity")
        self.add_node(required_equity_operation)

        self.add_transition(self.get_signal("krav_total_ramme"),
                            required_equity_operation,
                            label="thread")
        self.add_transition(self.get_signal("krav_belaning"),
                            required_equity_operation,
                            label="thread")

        required_equity = required_equity_operation.run(money=True, rnd=0)
        required_equity_signal = Signal(required_equity,
                                        "Calculated Required Equity",
                                        prettify_keys=True, length=10)

        self.add_signal(required_equity_signal, "krav_egenkapital")

        self.add_transition(required_equity_operation, required_equity_signal,
                            label="thread")

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

        fixed_payment_operation = FixedPayment(
            interest.data['krav_stresstest_annuitet'],
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
        self.add_transition(fixed_payment_operation, fixed_payment_signal,
                            label="thread")

    @Profiling
    @Debugger
    def converter_1(self):
        """
        method for converting Repayment Ability to monthly values

        """
        interval = self.get_signal("interval")
        fixed_amount = self.get_signal("fixed_amount")

        converter_operation = Converter(fixed_amount.data,
                                        interval.data['intervall'], 'Månedlig')
        self.add_node(converter_operation)

        self.add_transition(interval, converter_operation, label="thread")
        self.add_transition(fixed_amount, converter_operation, label="thread")

        converter = converter_operation.run()

        converter_signal = Signal(converter, "Calculated Monthly Fixed Amount")
        self.add_signal(converter_signal, "fixed_amount_monthly")
        self.add_transition(converter_operation, converter_signal,
                            label="thread")

    @Profiling
    @Debugger
    def converter_2(self):
        """
        method for converting Repayment Ability to plan values

        """
        interval = self.get_signal("interval")
        repayment_ability = self.get_signal("betjeningsevne")

        repayment_ability_converter_operation = Converter(repayment_ability.data,
                                                          'Månedlig',
                                                          interval.data[
                                                              'intervall'])
        self.add_node(repayment_ability_converter_operation)
        self.add_transition(interval, repayment_ability_converter_operation,
                            label="thread")
        self.add_transition(repayment_ability, repayment_ability_converter_operation,
                            label="thread")

        repayment_ability_fixed = repayment_ability_converter_operation.run()
        repayment_ability_fixed[
            'betjeningsevne_plan_annuitet'] = repayment_ability_fixed.pop(
            'betjeningsevne_2')

        repayment_ability_fixed_signal = Signal(repayment_ability_fixed,
                                                "Converted Fixed Repayment Ability Plan")
        self.add_signal(repayment_ability_fixed_signal, "repayment_ability_plan_fixed")
        self.add_transition(repayment_ability_converter_operation,
                            repayment_ability_fixed_signal,
                            label="thread")

        repayment_ability_fixed_mnd = {"betjeningsevne_mnd_annuitet":
                                           repayment_ability.data['betjeningsevne_2']}
        repayment_ability_fixed_mnd_signal = Signal(repayment_ability_fixed_mnd,
                                                    "Monthly Fixed Repayment Ability Plan")
        self.add_signal(repayment_ability_fixed_mnd_signal,
                        "repayment_ability_mnd_fixed")
        self.add_transition(repayment_ability_converter_operation,
                            repayment_ability_fixed_mnd_signal,
                            label="thread")

        repayment_ability_series = {"betjeningsevne_plan_serie":
                                        self.get_signal(
                                            'repayment_ability_plan_fixed').data[
                                            'betjeningsevne_plan_annuitet']}
        repayment_ability_series_signal = Signal(repayment_ability_series,
                                                 "Converted Series Repayment Ability Plan")
        self.add_signal(repayment_ability_series_signal,
                        "repayment_ability_plan_series")
        self.add_transition(repayment_ability_converter_operation,
                            repayment_ability_series_signal,
                            label="thread")

        repayment_ability_series_mnd = {"betjeningsevne_mnd_serie":
                                            repayment_ability.data[
                                                'betjeningsevne_2']}
        repayment_ability_series_mnd_signal = Signal(repayment_ability_series_mnd,
                                                     "Monthly Series Repayment Ability Plan")
        self.add_signal(repayment_ability_series_mnd_signal,
                        "repayment_ability_mnd_series")
        self.add_transition(repayment_ability_converter_operation,
                            repayment_ability_series_mnd_signal,
                            label="thread")

    @Profiling
    @Debugger
    def fixed_mortgage_payment_plan(self):
        """
        method for generating fixed mortgage plan

        """
        nominal_interest = self.get_signal("nominal_interest")
        fixed_stress_rate = self.get_signal("fixed_stress_test")
        if nominal_interest.data:
            interest = nominal_interest.data['nominell_rente']
        else:
            interest = fixed_stress_rate.data['stresstest_annuitet']
        period = self.get_signal("period")
        interval = self.get_signal("interval")
        amount = self.get_signal("belaning")
        start_date = self.get_signal("start_date")

        fixed_payment_plan_operation = GenerateFixedPaymentPlan(
            interest,
            period.data['laneperiode'],
            interval.data['intervall'],
            amount.data['belaning'],
            start_date.data['startdato'])

        self.add_node(fixed_payment_plan_operation)

        if nominal_interest.data:
            self.add_transition(nominal_interest, fixed_payment_plan_operation,
                                label="thread")
        self.add_transition(fixed_stress_rate, fixed_payment_plan_operation,
                            label="thread")
        self.add_transition(period, fixed_payment_plan_operation,
                            label="thread")
        self.add_transition(interval, fixed_payment_plan_operation,
                            label="thread")
        self.add_transition(amount, fixed_payment_plan_operation,
                            label="thread")
        self.add_transition(start_date, fixed_payment_plan_operation,
                            label="thread")

        fixed_payment_plan = fixed_payment_plan_operation.run()

        fixed_payment_plan_signal = Signal(fixed_payment_plan,
                                           "Generate Fixed Mortgage\n Payment Plan",
                                           prettify_keys=True, length=4)
        self.add_signal(fixed_payment_plan_signal, "fixed_payment_plan")
        self.add_transition(fixed_payment_plan_operation,
                            fixed_payment_plan_signal, label="thread")

    @Profiling
    @Debugger
    def series_mortgage_payment_plan(self):
        """
        method for generating series mortgage plan

        """
        nominal_interest = self.get_signal("nominal_interest")
        series_stress_rate = self.get_signal("serial_stress_test")
        if nominal_interest.data:
            interest = nominal_interest.data['nominell_rente']
        else:
            interest = series_stress_rate.data['stresstest_serie']
        period = self.get_signal("period")
        interval = self.get_signal("interval")
        amount = self.get_signal("belaning")
        start_date = self.get_signal("start_date")

        series_payment_plan_operation = GenerateSeriesPaymentPlan(
            interest,
            period.data['laneperiode'],
            interval.data['intervall'],
            amount.data['belaning'],
            start_date.data['startdato'])

        self.add_node(series_payment_plan_operation)

        if nominal_interest.data:
            self.add_transition(nominal_interest, series_payment_plan_operation,
                                label="thread")
        self.add_transition(series_stress_rate, series_payment_plan_operation,
                            label="thread")
        self.add_transition(period, series_payment_plan_operation,
                            label="thread")
        self.add_transition(interval, series_payment_plan_operation,
                            label="thread")
        self.add_transition(amount, series_payment_plan_operation,
                            label="thread")
        self.add_transition(start_date, series_payment_plan_operation,
                            label="thread")

        series_payment_plan = series_payment_plan_operation.run()

        series_payment_plan_signal = Signal(series_payment_plan,
                                            "Generate Series Mortgage\n Payment Plan",
                                            prettify_keys=True, length=4)
        self.add_signal(series_payment_plan_signal, "series_payment_plan")
        self.add_transition(series_payment_plan_operation,
                            series_payment_plan_signal,
                            label="thread")

    @Profiling
    @Debugger
    def extract_9(self):
        """
        method for extracting termin_aar_annuitet

        """
        fixed_payment_plan = self.get_signal("fixed_payment_plan")
        extract_total_periods_operation = Extract(fixed_payment_plan.data,
                                                  "total_termin_annuitet")
        self.add_node(extract_total_periods_operation)
        self.add_transition(fixed_payment_plan, extract_total_periods_operation,
                            label="thread")

        extract_total_periods = extract_total_periods_operation.run()

        extract_total_periods_signal = Signal(extract_total_periods,
                                              "Total number of\n Periods "
                                              "in Fixed Mortgage\n Payment Plan")

        self.add_signal(extract_total_periods_signal,
                        "total_periods_fixed_plan")
        self.add_transition(extract_total_periods_operation,
                            extract_total_periods_signal, label="thread")

    @Profiling
    @Debugger
    def extract_10(self):
        """
        method for extracting termin_belop_annuitet

        """
        fixed_payment_plan = self.get_signal("fixed_payment_plan")
        extract_total_amount_operation = Extract(fixed_payment_plan.data,
                                                 "total_belop_annuitet")
        self.add_node(extract_total_amount_operation)
        self.add_transition(fixed_payment_plan, extract_total_amount_operation,
                            label="thread")

        extract_total_amount = extract_total_amount_operation.run()

        extract_total_amount_signal = Signal(extract_total_amount,
                                             "Total Amount Paid in\n "
                                             "Fixed Mortgage\n Payment Plan")

        self.add_signal(extract_total_amount_signal, "total_amount_fixed_plan")
        self.add_transition(extract_total_amount_operation,
                            extract_total_amount_signal, label="thread")

    @Profiling
    @Debugger
    def division_4(self):
        """
        method for calculating average payment per period

        """
        total_amount_fixed_plan = self.get_signal("total_amount_fixed_plan")
        total_periods_fixed_plan = self.get_signal("total_periods_fixed_plan")

        required_total_frame_operation = Division(
            {"snitt_total_termin_belop_annitet":
                 total_amount_fixed_plan.data[
                     "total_belop_annuitet"]},
            total_periods_fixed_plan.data,
            "Calculate Average\n Total Payment in Fixed\n Payment Plan")
        self.add_node(required_total_frame_operation)

        self.add_transition(total_amount_fixed_plan,
                            required_total_frame_operation,
                            label="thread")
        self.add_transition(total_periods_fixed_plan,
                            required_total_frame_operation,
                            label="thread")

        average_total_amount_fixed_plan = required_total_frame_operation.run(
            percent=False,
            money=True)

        average_total_amount_fixed_plan_signal = Signal(
            average_total_amount_fixed_plan,
            "Calculated Average\n "
            "Total Payment in Fixed\n "
            "Payment Plan",
            prettify_keys=True, length=10)

        self.add_signal(average_total_amount_fixed_plan_signal,
                        "average_total_amount_fixed")

        self.add_transition(required_total_frame_operation,
                            average_total_amount_fixed_plan_signal,
                            label="thread")

    @Profiling
    @Debugger
    def converter_3(self):
        """
        method for converting average payment per period into monthly

        """
        interval = self.get_signal("interval")
        average_total_amount_fixed = self.get_signal("average_total_amount_fixed")

        average_total_amount_fixed_converted_operation = Converter(average_total_amount_fixed.data,
                                                                   interval.data['intervall'],
                                                                   'Månedlig')
        self.add_node(average_total_amount_fixed_converted_operation)
        self.add_transition(interval, average_total_amount_fixed_converted_operation,
                            label="thread")
        self.add_transition(average_total_amount_fixed,
                            average_total_amount_fixed_converted_operation,
                            label="thread")

        average_total_amount_fixed_converted = average_total_amount_fixed_converted_operation.run()

        average_total_amount_fixed_converted_signal = Signal(average_total_amount_fixed_converted,
                                                             "Converted Average\n Total Payment in "
                                                             "Fixed\n Payment Plan")
        self.add_signal(average_total_amount_fixed_converted_signal,
                        "average_total_amount_fixed_converted")
        self.add_transition(average_total_amount_fixed_converted_operation,
                            average_total_amount_fixed_converted_signal,
                            label="thread")

    @Profiling
    @Debugger
    def subtraction_4(self):
        """
        subtract operation to calculate net liquidity based on fixed rate plan after restructuring

        """
        repayment_ability_mnd_fixed = self.get_signal("repayment_ability_mnd_fixed")
        average_total_amount_fixed_converted = self.get_signal("average_total_amount_fixed_converted")

        average_net_liquidity_mnd_fixed_operation = Subtraction(
            {"nettolikviditet_annuitet": repayment_ability_mnd_fixed.data[
                'betjeningsevne_mnd_annuitet']},
            average_total_amount_fixed_converted.data,
            "Calculate Average Monthly Net Liquidity "
            "for Fixed Plan")
        self.add_node(average_net_liquidity_mnd_fixed_operation)
        self.add_transition(repayment_ability_mnd_fixed, average_net_liquidity_mnd_fixed_operation)
        self.add_transition(average_total_amount_fixed_converted, average_net_liquidity_mnd_fixed_operation)

        average_net_liquidity_mnd_fixed = average_net_liquidity_mnd_fixed_operation.run(money=True, rnd=0)

        average_net_liquidity_mnd_fixed_signal = Signal(average_net_liquidity_mnd_fixed,
                                                        "Calculated Average Monthly Net Liquidity for "
                                                        "Fixed Plan")

        self.add_signal(average_net_liquidity_mnd_fixed_signal, "nettolikviditet_annuitet")
        self.add_transition(average_net_liquidity_mnd_fixed_operation, average_net_liquidity_mnd_fixed_signal)

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
        repayment_ability = self.get_signal("betjeningsevne")
        yearly_income = self.get_signal("arsinntekt_aar")
        mortgage_limit = self.get_signal("belaning")
        equity_share = self.get_signal("egenkapital_andel")
        mortgage_share = self.get_signal("belaningsgrad")
        total_financing_frame = self.get_signal("total_ramme")
        max_mortgage_limit = self.get_signal("krav_belaning_maks")
        required_mortgage_limit = self.get_signal("krav_belaning")
        required_equity_share = self.get_signal("krav_egenkapital_andel")
        required_mortgage_share = self.get_signal("krav_belaningsgrad")
        required_total_financing_frame = self.get_signal("krav_total_ramme")
        required_equity = self.get_signal("krav_egenkapital")
        fixed_amount = self.get_signal("fixed_amount_monthly")
        fixed_payment_plan = self.get_signal("fixed_payment_plan")
        series_payment_plan = self.get_signal("series_payment_plan")
        repayment_ability_plan_fixed = self.get_signal("repayment_ability_plan_fixed")
        repayment_ability_mnd_fixed = self.get_signal("repayment_ability_mnd_fixed")
        repayment_ability_plan_series = self.get_signal("repayment_ability_plan_series")
        repayment_ability_mnd_series = self.get_signal("repayment_ability_mnd_series")
        average_total_amount_fixed_converted = self.get_signal(
            "average_total_amount_fixed_converted")
        average_net_liquidity_mnd_fixed = self.get_signal("nettolikviditet_annuitet")

        multiplex_operation = Multiplex([fixed_stress_rate, serial_stress_rate,
                                         required_fixed_rates,
                                         required_serial_rates, equity,
                                         repayment_ability, yearly_income,
                                         mortgage_limit, equity_share,
                                         mortgage_share, total_financing_frame,
                                         max_mortgage_limit,
                                         required_mortgage_limit,
                                         required_equity_share,
                                         required_mortgage_share,
                                         required_total_financing_frame,
                                         required_equity, fixed_amount,
                                         fixed_payment_plan,
                                         series_payment_plan,
                                         repayment_ability_plan_fixed,
                                         repayment_ability_mnd_fixed,
                                         repayment_ability_plan_series,
                                         repayment_ability_mnd_series,
                                         average_total_amount_fixed_converted,
                                         average_net_liquidity_mnd_fixed],
                                        "Multiplex Restructured Mortgage Information")

        self.add_node(multiplex_operation)

        self.add_transition(fixed_stress_rate, multiplex_operation)
        self.add_transition(serial_stress_rate, multiplex_operation)
        self.add_transition(required_fixed_rates, multiplex_operation)
        self.add_transition(required_serial_rates, multiplex_operation)
        self.add_transition(equity, multiplex_operation)
        self.add_transition(repayment_ability, multiplex_operation)
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
        self.add_transition(repayment_ability_plan_fixed, multiplex_operation)
        self.add_transition(repayment_ability_mnd_fixed, multiplex_operation)
        self.add_transition(repayment_ability_plan_series, multiplex_operation)
        self.add_transition(repayment_ability_mnd_series, multiplex_operation)
        self.add_transition(average_total_amount_fixed_converted, multiplex_operation)
        self.add_transition(average_net_liquidity_mnd_fixed, multiplex_operation)

        multiplex = multiplex_operation.run()
        multiplex_signal = Signal(multiplex,
                                  "Multiplexed Restructure Mortgage Information",
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
        output_operation = OutputOperation(
            "Multiplexed Restructure Information")
        self.add_node(output_operation)
        self.add_transition(restructure_information, output_operation)

        output_signal = OutputSignal(restructure_information.data,
                                     desc="Multiplexed Restructure Information",
                                     prettify_keys=True,
                                     length=4)
        self.add_signal(output_signal, "output_data")
        self.add_transition(output_operation, output_signal)
        self.print_pdf()

        return restructure_information.data
