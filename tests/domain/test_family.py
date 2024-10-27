# -*- coding: utf-8 -*-

"""
Tests for family entity class

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from uuid import UUID
from abc import ABC

import pytest as pt

from source.domain import Family, Female, Entity, Male


class TestFamily:
    """
    Test class for the entity Family()

    """

    def setup_method(self):
        """
        Executed before all tests

        """
        self.family_members = [Male(age=39), Female(age=40)]
        self.family = Family(self.family_members, select_year=2021)

    @classmethod
    def teardown(cls):
        """
        Executed after all tests

        """
        cls.family = None

    def test_family_object_is_instance_of_family_and_abc(self):
        """
        Test that all family objects are instances of Family class and Abstract Base Class (ABC)

        """
        for parent in [Entity, ABC]:
            isinstance(self.family, parent)
            issubclass(self.family.__class__, parent)

    @pt.mark.parametrize('invalid_arg', [True, 'test', 90210, 90210.0, ('test', 'test'), {}])
    def test_family_members_type_are_list(self, invalid_arg):
        """
        Test that Family object raises TypeError if family_members argument are invalid

        """
        with pt.raises(TypeError):
            self.family.familie_medlemmer = invalid_arg

    @staticmethod
    @pt.mark.parametrize('invalid_arg', [True, 'test', 90210, 90210.0, ('test', 'test'), {}])
    def test_family_members_type_are_list_constructor(invalid_arg):
        """
        Test that Family object raises TypeError if family_members argument are invalid

        """
        with pt.raises(TypeError):
            Family(invalid_arg, income=invalid_arg, fossil_cars=invalid_arg)

    @pt.mark.parametrize('invalid_arg', [(), {}, []])
    def test_income_and_cars_tracking_error_for_invalid_arguments(self, invalid_arg):
        """
        TypeError raised when invalid income and cars argument types passed into Family class
        through setter

        """
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
        with pt.raises(ValueError):
            self.family.inntekt = negative_income
        with pt.raises(ValueError):
            self.family.antall_biler = negative_cars

    @pt.mark.parametrize('inntekt', [594400, 594400, '594400', '594400'])
    @pt.mark.parametrize('antall_biler', [0, '0'])
    def test_arguments_gets_set_in_family_object(self, inntekt, antall_biler):
        """
        Test that valid arguments gets set into object

        """
        family = self.family
        new_family = [Male(25), Female(24)]

        family.familie_medlemmer = new_family
        family.inntekt = inntekt
        family.antall_biler = antall_biler

        assert family.familie_medlemmer == new_family
        assert family.inntekt == str(inntekt)
        assert family.antall_biler == str(antall_biler)

    @staticmethod
    @pt.mark.parametrize('inntekt', [594400, 594400, '594400', '594400'])
    @pt.mark.parametrize('antall_biler', [0, '0'])
    def test_arguments_gets_set_in_family_object_constructor(inntekt, antall_biler):
        """
        Test that valid arguments gets set into object through constructor

        """
        new_family = [Male(25), Female(24)]
        family = Family(new_family, inntekt, antall_biler, select_year=2021)

        assert family.familie_medlemmer == new_family
        assert family.inntekt == str(inntekt)
        assert family.antall_biler == str(antall_biler)

    def test_add_family_members_method(self):
        """
        Test the add_family_members method in Family class

        """
        family = self.family
        children = [Male(age=12), Female(age=10)]
        family.add_family_members(children)
        assert len(family.familie_medlemmer) == 4

        child = Male(age=5)
        family.add_family_members(child)
        assert len(family.familie_medlemmer) == 5

    @staticmethod
    def test_get_properties_method():
        """
        Test get properties method in Family class

        """
        family = [Male(age=48), Female(age=45, pregnant='1'), Female(age=17), Male(age=13, sfo='1'),
                  Female(age=5, kinder_garden='1')]
        properties = {'inntekt': '1489000', 'antall_biler': '2', 'antall_elbiler': '0',
                      'select_year': '2021'}
        for i, member in enumerate(family):
            for key, value in member.__dict__.items():
                if "_id" not in key:
                    properties.update({key[1:] + str(i): value})

        fam = Family(family, income=1489000, fossil_cars=2, select_year=2021)

        assert fam.sifo_properties() == properties

    def test_that_id_not_in_sifo_properties(self):
        """
        Test that sifo_properties() does not include entity id's

        """
        prop = self.family.sifo_properties()
        assert 'id' not in prop.keys()

    def test_family_object_id_are_uuid4(self):
        """
        Test that all entity ids are uuid4 compatible

        """
        assert UUID(str(self.family.id_))

    def test_rules_in_family(self):
        """
        Test that rules are included in Family object

        """
        rules = ["non_negative_income", "non_negative_cars", "kindergarten_criteria",
                 "sfo_criteria", "pregnant_criteria"]
        assert Family.rules() == ", ".join(rules).replace("'", "")
        assert self.family.rules() == ", ".join(rules).replace("'", "")

    @pt.mark.parametrize('invalid_year', ['', None, (), {}, []])
    def test_validate_select_year(self, invalid_year):
        """
        Test validate_select_year method in Family object

        """
        with pt.raises(ValueError):
            self.family.validate_select_year(invalid_year)

    @pt.mark.parametrize('year', ['2022', '2021'])
    def test_select_year_setter(self, year):
        """
        Test select year setter in Family object

        """
        self.family.select_year = year
        assert self.family.select_year == year
