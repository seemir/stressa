# -*- coding: utf-8 -*-

"""
Tax form entity class implementation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from typing import Union

from datetime import date

from source.util import Assertor, Debugger

from source.domain.entity import Entity


class TaxForm(Entity):
    """
    Tax form entity class

    """

    tax_version_mapping = {'2022': ('skatteberegningsgrunnlagV7', 'skattepliktV9'),
                           '2021': ('skatteberegningsgrunnlagV6', 'skattepliktV8'),
                           '2020': ('skattegrunnlagV6', 'skattepliktV7'),
                           '2019': ('skattegrunnlagV5', 'skattepliktV6'),
                           '2018': ('skattegrunnlagV5', 'skattepliktV5')}

    @staticmethod
    def validate_tax_year(tax_year: Union[int, float, str]):
        """
        Method for validating tax, i.e. insure that year is of
        correct datatype and in calculation range

        Parameters
        ----------
        tax_year        : int, float, str
                          year to be validated

        """
        Assertor.assert_data_types([tax_year], [(int, float, str)])
        Assertor.assert_arguments([str(tax_year)],
                                  [{'year': tuple(TaxForm.tax_version_mapping.keys())}])

    @staticmethod
    def validate_age(age: Union[int, float, str]):
        """
        Method for validating age of individual

        Parameters
        ----------
        age           : int, float, str
                        age to be validated

        """
        Assertor.assert_data_types([age], [(int, float, str)])
        Assertor.assert_non_negative(age, "Only non-negative 'age' accepted")

    @staticmethod
    def validate_tax_form_values(values: list):
        """
        Method for validating numeric values

        Parameters
        ----------
        values         : int, float, str
                         value to be validated

        """
        for value in values:
            Assertor.assert_data_types([value], [(int, float, str)])
            Assertor.assert_non_negative(value, "Tax form values cannot be negative")

    def __init__(self, age: Union[str, int],
                 income: Union[str, int, float],
                 tax_year: Union[str, int] = date.today().year,
                 interest_income: Union[str, int, float] = 0,
                 interest_cost: Union[str, int, float] = 0,
                 value_of_real_estate: Union[str, int, float] = 0,
                 bank_deposit: Union[str, int, float] = 0,
                 debt: Union[str, int, float] = 0):

        """
        Constructor / Instantiate the class

        Parameters
        ----------
        age                 : str, int
                              age of individual
        income              : str, int, float
                              income of individual
        tax_year            : str, int
                              tax year to calculate taxes
        interest_income     : str, int, float
                              income of interest
        interest_cost       : str, int, float
                              cost of income
        value_of_real_estate: str, int, float
                              value of real-estate (if any applies)
        bank_deposit        : str, int, float
                              value of bank deposit
        debt                : str, int, float
                              total debt

        """

        try:
            super().__init__()

            self.validate_age(age)
            self.validate_tax_form_values(
                [income, interest_income, interest_cost, value_of_real_estate, bank_deposit, debt])
            self.validate_tax_year(tax_year)

            self._age = str(age)
            self._income = str(income)
            self._tax_year = str(date.today().year) if not \
                tax_year else str(tax_year)
            self._interest_income = str(0) if not interest_income else str(interest_income)
            self._interest_cost = str(0) if not interest_cost else str(interest_cost)
            self._value_of_real_estate = str(0) if not value_of_real_estate \
                else str(value_of_real_estate)
            self._bank_deposit = str(0) if not bank_deposit else str(bank_deposit)
            self._debt = str(0) if not debt else str(debt)

        except Exception as tax_form_exception:
            raise tax_form_exception

    @property
    def age(self):
        """
        age getter

        Returns
        -------
        out         : str
                      active age in tax_form

        """
        return self._age

    @age.setter
    def age(self, new_age: Union[str, int, float]):
        """
        age setter

        Parameters
        ----------
        new_age     : str, int, float
                      new age to apply

        """
        self.validate_age(new_age)
        self._age = str(new_age)

    @property
    def income(self):
        """
        income getter

        Returns
        -------
        out         : str
                      active income in taxform

        """
        return self._income

    @income.setter
    def income(self, new_income: Union[str, int, float]):
        """
        income setter

        Parameters
        ----------
        new_income  : str, int, float
                      new income to set in object

        """
        self.validate_tax_form_values([new_income])
        self._income = str(new_income)

    @property
    def tax_year(self):
        """
        tax_year getter

        Returns
        -------
        out         : str
                      active tax_year in taxform

        """
        return self._tax_year

    @tax_year.setter
    def tax_year(self, new_tax_year: Union[str, int, float]):
        """
        tax_year setter

        Parameters
        ----------
        new_tax_year  : str, int, float
                        new tax_year to set in object

        """
        self.validate_tax_form_values([new_tax_year])
        self._tax_year = str(new_tax_year)

    @property
    def interest_income(self):
        """
        interest_income getter

        Returns
        -------
        out         : str
                      active interest_income in taxform

        """
        return self._interest_income

    @interest_income.setter
    def interest_income(self, new_interest_income: Union[str, int, float]):
        """
        new_interest_income setter

        Parameters
        ----------
        new_interest_income  : str, int, float
                               new interest_income to set in object

        """
        self.validate_tax_form_values([new_interest_income])
        self._interest_income = str(new_interest_income)

    @property
    def interest_cost(self):
        """
        interest_cost getter

        Returns
        -------
        out         : str
                      active interest_cost in taxform

        """
        return self._interest_cost

    @interest_cost.setter
    def interest_cost(self, new_interest_cost: Union[str, int, float]):
        """
        new_interest_cost setter

        Parameters
        ----------
        new_interest_cost  : str, int, float
                             new interest_cost to set in object

        """
        self.validate_tax_form_values([new_interest_cost])
        self._interest_cost = str(new_interest_cost)

    @property
    def value_of_real_estate(self):
        """
        value_of_real_estate getter

        Returns
        -------
        out         : str
                      value_of_real_estate in taxform

        """
        return self._value_of_real_estate

    @value_of_real_estate.setter
    def value_of_real_estate(self, new_value_of_real_estate: Union[str, int, float]):
        """
        value_of_real_estate setter

        """
        self.validate_tax_form_values([new_value_of_real_estate])
        self._value_of_real_estate = str(new_value_of_real_estate)

    @property
    def bank_deposit(self):
        """
        bank_deposit getter

        Returns
        -------
        out         : str
                      active bank_deposit in taxform

        """
        return self._bank_deposit

    @bank_deposit.setter
    def bank_deposit(self, new_bank_deposit: Union[str, int, float]):
        """
        new_bank_deposit setter

        Parameters
        ----------
        new_bank_deposit  : str, int, float
                            new bank_deposit to set in object

        """
        self.validate_tax_form_values([new_bank_deposit])
        self._bank_deposit = str(new_bank_deposit)

    @property
    def debt(self):
        """
        debt getter

        Returns
        -------
        out         : str
                      active debt in taxform

        """
        return self._debt

    @debt.setter
    def debt(self, new_debt: Union[str, int, float]):
        """
        new_debt setter

        Parameters
        ----------
        new_debt  : str, int, float
                    new debt to set in object

        """
        self.validate_tax_form_values([new_debt])
        self._debt = str(new_debt)

    @Debugger
    def tax_form_properties(self):
        """
        returns all active tax form properties

        Returns
        -------
        Out         : dict
                      dictionary of all active properties

        """
        properties = dict(list(self.__dict__.items()))
        del properties['_id']
        properties.update({'tax_year_config': self.tax_version_mapping[self.tax_year]})
        return properties

    @staticmethod
    def rules():
        """
        all active validation rules in entity

        Returns
        -------
        out         : dict
                      dictionary with all the active rules in the entity

        """
        return ", ".join(
            ['non_negative_age', 'non_negative_income', 'non_negative_interest_income',
             '\\nnon_negative_interest_cost', 'non_negative_value_of_real_estate',
             'non_negative_bank_deposit', '\\nnon_negative_debt',
             'tax_year_criteria']).replace("'", "")
