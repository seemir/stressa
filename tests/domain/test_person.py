# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.exception.base_class_cannot_be_instantiated import BaseClassCannotBeInstantiated
from source.domain.person import Person
import pytest as pt


class TestPerson:

    @pt.mark.parametrize('age', [18])
    @pt.mark.parametrize('sifo_age', ['19'])
    def test_can_access_static_set_age(self, age, sifo_age):
        """
        Test that it is possible to access the static set_age() method

        """
        assert Person.set_age(age) == sifo_age

    @pt.mark.parametrize('age', [18, 18.0, '18', '18.0', 'test', (), [], {}])
    def test_set_age_with_different_data_types(self, age):
        """
        Test that set_age() method accepts only (int, float, str)

        """
        try:
            assert Person.set_age(age) == '19'
        except TypeError:
            with pt.raises(TypeError):
                Person.set_age(age)

    @pt.mark.parametrize('negative_age', [-18, -18.0, '-18', '-18.0'])
    def test_only_non_negative_numbers_accepted(self, negative_age):
        """
        Test only non-negative numbers can be passed to the set_age() method

        """
        with pt.raises(ValueError):
            Person.set_age(negative_age)

    @pt.mark.parametrize('yrs', [0.42, 0.92, 1, 2, 3, 5, 9, 13, 17, 19, 50, 60, 66, 75])
    def test_sifo_age_corner_cases(self, yrs):
        """
        Test all corner cases of set_age() method

        """
        for limit in [yrs - 0.05, yrs]:
            assert Person.set_age(limit) == str(yrs)
