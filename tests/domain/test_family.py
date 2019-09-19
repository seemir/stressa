# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.domain.female import Female
from source.domain.family import Family
from source.domain.male import Male
import pytest as pt


class TestFamily:

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.family = Family([Male(age=39), Female(age=40)])

    @classmethod
    def teardown(cls):
        """
        Executed after all tests

        """
        cls.family = None

    def test_family_object_is_instance_of_family(self):
        """
        Test that all family objects are instances of Family class

        """
        assert isinstance(self.family, Family)

    @pt.mark.parametrize('invalid_arg', [True, 'test', 90210, 90210.0, ('test', 'test'), {'test'}])
    def test_family_members_type_are_list(self, invalid_arg):
        """
        Test that Family object raises TypeError if family_members argument are invalid

        """
        family = self.family
        with pt.raises(TypeError):
            Family(invalid_arg)
        with pt.raises(TypeError):
            family.family_members = invalid_arg
        with pt.raises(TypeError):
            family.family_members = list(invalid_arg)

    @pt.mark.parametrize('invalid_arg', [(), {}])
    def test_income_and_cars_type_error_for_invalid_arguments(self, invalid_arg):
        """
        TypeError raised when invalid income and cars argument types passed into Family class
        through constructor or setter

        """
        family = self.family
        with pt.raises(TypeError):
            Family(family.family_members, income=invalid_arg)
        with pt.raises(TypeError):
            Family(family.family_members, cars=invalid_arg)
        with pt.raises(TypeError):
            family.inntekt = invalid_arg
        with pt.raises(TypeError):
            family.antall_biler = invalid_arg

    @pt.mark.parametrize('negative_income', [-1094400, -1094400.0, '-1094400', '-1094400.0'])
    @pt.mark.parametrize('negative_cars', [-1, '-1'])
    def test_income_and_cars_cannot_be_negative(self, negative_income, negative_cars):
        """
        Test that ValueError is raised if negative values for income and cars are passed into
        Family class through constructor or setter

        """
        family = self.family
        with pt.raises(ValueError):
            Family(family.family_members, income=negative_income)
        with pt.raises(ValueError):
            Family(family.family_members, cars=negative_cars)
        with pt.raises(ValueError):
            family.inntekt = negative_income
        with pt.raises(ValueError):
            family.antall_biler = negative_cars

    @pt.mark.parametrize('income', [1094400, 1094400.0, '1094400', '1094400.0'])
    @pt.mark.parametrize('cars', [1, '1'])
    def test_arguments_gets_set_in_family_object(self, income, cars):
        """
        Test that valid arguments gets set into object when passed through constructor or setter

        """

