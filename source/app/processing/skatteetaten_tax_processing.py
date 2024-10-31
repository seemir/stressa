# -*- coding: utf-8 -*-

"""
Process for validating tax form

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking, Profiling, Debugger

from .engine import Process, Signal, InputOperation, ValidateTaxForm, \
    SkatteetatenTaxInfoConnector, OutputOperation, OutputSignal, Extract, Division, Multiplex, \
    Flatten, Factor


class SkatteetatenTaxProcessing(Process):
    """
    Process for tax calculating given Skatteetaten rules

    """

    @Tracking
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
        self.skatteetaten_tax_info_connector()

        self.run_parallel([self.extract_1, self.extract_2, self.extract_3])
        self.factor()
        self.run_parallel([self.divide_1, self.divide_2, self.divide_3])
        self.multiplex()
        self.flatten()

        self._skatteetaten_tax_info = self.output_operation()
        self.end_process()

    @property
    def skatteetaten_tax_info(self):
        """
        skatteetaten tax info getter

        Returns
        -------
        out         : dict
                      dictionary with tax info

        """
        return self._skatteetaten_tax_info

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
        tax_form_signal = Signal(tax_form, "Validated Tax Form Information", prettify_keys=True,
                                 length=6)
        self.add_signal(tax_form_signal, "validated_tax_form")

        self.add_transition(validate_tax_form_operation, tax_form_signal)

    @Profiling
    @Tracking
    def skatteetaten_tax_info_connector(self):
        """
        method for retrieve Skatteetaten tax info

        """
        validated_tax_form = self.get_signal("validated_tax_form")
        skatteetaten_tax_info_connector_operation = SkatteetatenTaxInfoConnector(
            validated_tax_form.data)
        self.add_node(skatteetaten_tax_info_connector_operation)

        self.add_transition(validated_tax_form, skatteetaten_tax_info_connector_operation)

        skatteetaten_tax_info = skatteetaten_tax_info_connector_operation.run()
        skatteetaten_tax_info_signal = Signal(skatteetaten_tax_info, "Skatteetaten Tax Information",
                                              prettify_keys=True, length=4)
        self.add_signal(skatteetaten_tax_info_signal, "skatteetaten_tax_info")

        self.add_transition(skatteetaten_tax_info_connector_operation, skatteetaten_tax_info_signal)

    @Profiling
    @Tracking
    def extract_1(self):
        """
        method for extracting total calculated taxes

        """
        skatteetaten_tax_info = self.get_signal("skatteetaten_tax_info")
        total_tax_extract_operation = Extract(skatteetaten_tax_info.data, "beregnet_skatt")
        self.add_node(total_tax_extract_operation)
        self.add_transition(skatteetaten_tax_info, total_tax_extract_operation, label="thread")

        total_tax_extract = total_tax_extract_operation.run()
        total_tax_extract_signal = Signal(total_tax_extract, "Skatteetaten Total Tax")

        self.add_signal(total_tax_extract_signal, "total_tax")
        self.add_transition(total_tax_extract_operation, total_tax_extract_signal, label="thread")

    @Profiling
    @Tracking
    def extract_2(self):
        """
        method for extracting income basis

        """
        skatteetaten_tax_info = self.get_signal("skatteetaten_tax_info")
        income_extract_operation = Extract(skatteetaten_tax_info.data,
                                           "sum_inntekter_i_alminnelig_inntekt_foer_"
                                           "fordelingsfradrag")
        self.add_node(income_extract_operation)
        self.add_transition(skatteetaten_tax_info, income_extract_operation, label="thread")

        income_extract = income_extract_operation.run()
        income_extract_signal = Signal(income_extract, "Skatteetaten Total Income Basis")

        self.add_signal(income_extract_signal, "total_income")
        self.add_transition(income_extract_operation, income_extract_signal, label="thread")

    @Profiling
    @Tracking
    def extract_3(self):
        """
        method for extracting total debt

        """
        skatteetaten_tax_info = self.get_signal("skatteetaten_tax_info")
        debt_extract_operation = Extract(skatteetaten_tax_info.data, "samlet_gjeld")
        self.add_node(debt_extract_operation)
        self.add_transition(skatteetaten_tax_info, debt_extract_operation, label="thread")

        debt_extract = debt_extract_operation.run()
        debt_extract_signal = Signal(debt_extract, "Skatteetaten Total Debt")

        self.add_signal(debt_extract_signal, "total_debt")
        self.add_transition(debt_extract_operation, debt_extract_signal, label="thread")

    @Profiling
    @Tracking
    def factor(self):
        """
        method for creating a factor

        """
        factor_operation = Factor("12", "Monthly factor conversion")
        self.add_node(factor_operation)

        factor = factor_operation.run()
        factor_signal = Signal(factor, "Monthly factor")

        self.add_signal(factor_signal, "monthly_factor")
        self.add_transition(factor_operation, factor_signal)

    @Profiling
    @Tracking
    def divide_1(self):
        """
        method for calculating tax percentage

        """

        tax_percentage = Division(
            {"skatteprosent": self.get_signal("total_tax").data["beregnet_skatt"]["beloep"]},
            self.get_signal("total_income").data,
            "Calculate Tax Share of Total Monthly Income")
        self.add_node(tax_percentage)

        self.add_transition(self.get_signal("total_income"), tax_percentage, label="thread")
        self.add_transition(self.get_signal("total_tax"), tax_percentage, label="thread")

        tax_share_of_monthly_income = tax_percentage.run()
        tax_share_of_monthly_income_signal = Signal(tax_share_of_monthly_income,
                                                    "Tax Share of Total Monthly Income",
                                                    prettify_keys=True, length=10)

        self.add_signal(tax_share_of_monthly_income_signal, "tax_share_of_monthly_income")

        self.add_transition(tax_percentage, tax_share_of_monthly_income_signal, label="thread")

    @Profiling
    @Tracking
    def divide_2(self):
        """
        method for calculating debt percentage

        """

        debt_level_operation = Division(
            {"gjeldsgrad": self.get_signal("total_debt").data["samlet_gjeld"]},
            self.get_signal("total_income").data,
            "Calculate Total Monthly Income Share of Debt")
        self.add_node(debt_level_operation)

        self.add_transition(self.get_signal("total_income"), debt_level_operation, label="thread")
        self.add_transition(self.get_signal("total_debt"), debt_level_operation, label="thread")

        debt_level = debt_level_operation.run(percent=False)
        debt_level_signal = Signal(debt_level, "Total Monthly Income Share of Debt",
                                   prettify_keys=True, length=10)

        self.add_signal(debt_level_signal, "debt_level")
        self.add_transition(debt_level_operation, debt_level_signal, label="thread")

    @Profiling
    @Tracking
    def divide_3(self):
        """
        method for calculating monthly tax payment

        """

        monthly_tax_operation = Division(
            {"beregnet_skatt_per_mnd_beloep": self.get_signal("total_tax").data["beregnet_skatt"][
                "beloep"]}, self.get_signal("monthly_factor").data,
            "Calculate Total Monthly Tax Cost")
        self.add_node(monthly_tax_operation)

        self.add_transition(self.get_signal("total_tax"), monthly_tax_operation, label="thread")
        self.add_transition(self.get_signal("monthly_factor"), monthly_tax_operation,
                            label="thread")

        monthly_tax = monthly_tax_operation.run(percent=False, money=True, rnd=0)

        monthly_tax_signal = Signal(monthly_tax, "Total Monthly Tax Cost",
                                    prettify_keys=True, length=10)

        self.add_signal(monthly_tax_signal, "monthly_tax")
        self.add_transition(monthly_tax_operation, monthly_tax_signal, label="thread")

    @Profiling
    @Tracking
    def multiplex(self):
        """
        method for multiplexing tax share with tax info

        """
        tax_share_of_monthly_income = self.get_signal("tax_share_of_monthly_income")
        debt_level = self.get_signal("debt_level")
        skatteetaten_tax_info = self.get_signal("skatteetaten_tax_info")
        monthly_tax = self.get_signal("monthly_tax")

        multiplex_operation = Multiplex(
            [tax_share_of_monthly_income, debt_level, skatteetaten_tax_info, monthly_tax],
            "Multiplex Tax Information")

        self.add_node(multiplex_operation)
        self.add_transition(tax_share_of_monthly_income, multiplex_operation)
        self.add_transition(debt_level, multiplex_operation)
        self.add_transition(skatteetaten_tax_info, multiplex_operation)
        self.add_transition(monthly_tax, multiplex_operation)

        multiplex = multiplex_operation.run()
        multiplex_signal = Signal(multiplex, "Multiplexed Tax Information", prettify_keys=True,
                                  length=4)
        self.add_signal(multiplex_signal, "multiplex_tax_info")
        self.add_transition(multiplex_operation, multiplex_signal)

    @Profiling
    @Tracking
    def flatten(self):
        """
        method for flattening multiplexed data

        """
        multiplex_tax_info = self.get_signal("multiplex_tax_info")

        flatten_operation = Flatten(multiplex_tax_info.data, "Flatten Multiplexed Tax Information")
        self.add_node(flatten_operation)
        self.add_transition(multiplex_tax_info, flatten_operation)

        flatten = flatten_operation.run()

        flatten_signal = Signal(flatten, "Flattened Multiplexed Tax Information",
                                prettify_keys=True, length=4)

        self.add_signal(flatten_signal, "flatten_multiplex_tax_info")
        self.add_transition(flatten_operation, flatten_signal)

    @Profiling
    @Tracking
    def output_operation(self):
        """
        final method call in process

        """
        flatten_multiplex_tax_info = self.get_signal("flatten_multiplex_tax_info")
        output_operation = OutputOperation("Skatteetaten Tax Information")
        self.add_node(output_operation)
        self.add_transition(flatten_multiplex_tax_info, output_operation)

        output_signal = OutputSignal(flatten_multiplex_tax_info.data,
                                     desc="Skatteetaten Tax Information", prettify_keys=True,
                                     length=4)
        self.add_signal(output_signal, "output_data")
        self.add_transition(output_operation, output_signal)
        self.print_pdf()

        return flatten_multiplex_tax_info.data
