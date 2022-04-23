# -*- coding: utf-8 -*-

"""
Tests for TaxForm entity class

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from uuid import UUID
from abc import ABC

import pytest as pt

from source.domain import TaxForm, Entity


class TestTaxForm:
    """
    Test class for the entity TaxForm

    """

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.tax_form = TaxForm(age=34, income=560000, tax_year=2022)

    @classmethod
    def teardown(cls):
        """
        Executed after all tests

        """
        cls.tax_form = None

    def test_tax_form_object_is_instance_of_tax_form_and_abc(self):
        """
        Test that all tax_form objects are instances of TaxForm class and Abstract Base Class (ABC)

        """
        for parent in [Entity, ABC]:
            isinstance(self.tax_form, parent)
            issubclass(self.tax_form.__class__, parent)

    @staticmethod
    @pt.mark.parametrize('invalid_arg', [('test', 'test'), {}])
    def test_tax_form_type(invalid_arg):
        """
        Test that tax_form object raises TypeError if argument are invalid

        """
        with pt.raises(TypeError):
            TaxForm(age=invalid_arg, income=invalid_arg, tax_year=invalid_arg)

    @pt.mark.parametrize('invalid_arg', [(), {}, []])
    def test_type_error_for_invalid_arguments(self, invalid_arg):
        """
        TypeError raised when invalid income and cars argument types passed into TaxForm class
        through setter

        """
        with pt.raises(TypeError):
            self.tax_form.income = invalid_arg
        with pt.raises(TypeError):
            self.tax_form.age = invalid_arg
        with pt.raises(TypeError):
            self.tax_form.tax_year = invalid_arg

    @pt.mark.parametrize('negative_income', [-1094400, -1094400.0, '-1094400', '-1094400.0'])
    @pt.mark.parametrize('negative_age', [-1, '-1'])
    @pt.mark.parametrize('negative_tax_year', [-2022, '-2022'])
    def test_income_age_and_tax_year_cannot_be_negative(self, negative_income, negative_age,
                                                        negative_tax_year):
        """
        Test that ValueError is raised if negative values for income, age or tax_year are passed
        into TaxForm class through constructor or setter

        """
        with pt.raises(ValueError):
            self.tax_form.income = negative_income
        with pt.raises(ValueError):
            self.tax_form.age = negative_age
        with pt.raises(ValueError):
            self.tax_form.tax_year = negative_tax_year

    @pt.mark.parametrize('income', [594400, '594400'])
    @pt.mark.parametrize('age', [34, '34'])
    @pt.mark.parametrize('tax_year', [2022, '2022'])
    @pt.mark.parametrize('interest_cost', [1000])
    @pt.mark.parametrize('interest_income', [500])
    @pt.mark.parametrize('bank_deposit', [100000])
    @pt.mark.parametrize('value_of_real_estate', [1000000])
    @pt.mark.parametrize('debt', [1000000])
    def test_arguments_gets_set_in_tax_form_object(self, income, age, tax_year, interest_cost,
                                                   interest_income, bank_deposit,
                                                   value_of_real_estate, debt):
        """
        Test that valid arguments gets set into object

        """
        tax_form = self.tax_form

        tax_form.income = income
        tax_form.age = age
        tax_form.tax_year = tax_year
        tax_form.interest_cost = interest_cost
        tax_form.interest_income = interest_income
        tax_form.bank_deposit = bank_deposit
        tax_form.value_of_real_estate = value_of_real_estate
        tax_form.debt = debt

        assert tax_form.income == str(income)
        assert tax_form.age == str(age)
        assert tax_form.tax_year == str(tax_year)
        assert tax_form.interest_cost == str(interest_cost)
        assert tax_form.interest_income == str(interest_income)
        assert tax_form.bank_deposit == str(bank_deposit)
        assert tax_form.value_of_real_estate == str(value_of_real_estate)
        assert tax_form.debt == str(debt)

    @staticmethod
    @pt.mark.parametrize('income', [594400, '594400'])
    @pt.mark.parametrize('age', [34, '34'])
    @pt.mark.parametrize('tax_year', [2022, '2022'])
    def test_arguments_gets_set_in_tax_form_object_constructor(income, age, tax_year):
        """
        Test that valid arguments gets set into object through constructor

        """
        tax_form = TaxForm(income=income, age=age, tax_year=tax_year)

        assert tax_form.income == str(income)
        assert tax_form.age == str(age)
        assert tax_form.tax_year == str(tax_year)

    def test_get_properties_method(self):
        """
        Test get properties method in tax_form class

        """
        assert self.tax_form.tax_form_properties() == {'_age': '34',
                                                       '_bank_deposit': '0',
                                                       '_bsu': '0',
                                                       '_debt': '0',
                                                       '_income': '560000',
                                                       '_interest_cost': '0',
                                                       '_interest_income': '0',
                                                       '_tax_year': '2022',
                                                       '_union_fee': '0',
                                                       '_value_of_real_estate': '0',
                                                       'tax_year_config': (
                                                       'skatteberegningsgrunnlagV7',
                                                       'skattepliktV9')}

    def test_that_id_not_in_tax_form_properties(self):
        """
        Test that tax_form_properties() does not include entity id's

        """
        prop = self.tax_form.tax_form_properties()
        assert 'id' not in prop.keys()

    def test_tax_form_object_id_are_uuid4(self):
        """
        Test that all entity ids are uuid4 compatible

        """
        assert UUID(str(self.tax_form.id_))

    def test_rules_in_tax_form(self):
        """
        Test that rules are included in tax_form object

        """
        rules = ['non_negative_age', 'non_negative_income', 'non_negative_interest_income',
                 '\\nnon_negative_interest_cost', 'non_negative_value_of_real_estate',
                 'non_negative_bank_deposit', '\\nnon_negative_debt',
                 'tax_year_criteria']
        assert self.tax_form.rules() == ", ".join(rules).replace("'", "")
