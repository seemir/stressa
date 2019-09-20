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
        cls.family_members = [Male(age=39), Female(age=40)]
        cls.family = Family(cls.family_members)

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
        with pt.raises(TypeError):
            Family(self.family_members, income=invalid_arg)
        with pt.raises(TypeError):
            Family(self.family_members, cars=invalid_arg)
        with pt.raises(TypeError):
            self.family.inntekt = invalid_arg
        with pt.raises(TypeError):
            self.family.antall_biler = invalid_arg

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

    @pt.mark.parametrize('inntekt', [1094400, 1094400.0, '1094400', '1094400.0'])
    @pt.mark.parametrize('antall_biler', [1, '1'])
    def test_arguments_gets_set_in_family_object_via_constr(self, inntekt, antall_biler):
        """
        Test that valid arguments gets set into object when passed through constructor

        """
        family_members = self.family_members
        family = Family(family_members, inntekt, antall_biler)
        assert family.family_members == family_members
        assert family.inntekt == str(inntekt)
        assert family.antall_biler == str(antall_biler)

    @pt.mark.parametrize('inntekt', [594400, 594400, '594400', '594400'])
    @pt.mark.parametrize('antall_biler', [0, '0'])
    def test_arguments_gets_set_in_family_object_via_setter(self, inntekt, antall_biler):
        """
        Test that valid arguments gets set into object when passed through setter

        """
        new_family = [Male(25), Female(24)]
        self.family.family_members = new_family
        self.family.inntekt = inntekt
        self.family.antall_biler = antall_biler

        assert self.family.family_members == new_family
        assert self.family.inntekt == str(inntekt)
        assert self.family.antall_biler == str(antall_biler)
