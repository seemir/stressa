# -*- coding: utf-8 -*-

"""
Test module for Person abstract base class entity

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from abc import ABC
import pytest as pt

from source.domain import Person
from source.util import TrackingError


class TestPerson:
    """
    Unittest for Person entity class

    """

    @classmethod
    def setup(cls):
        """
        runs before all tests

        """
        cls.person = Person()

    def test_person_is_instance_of_entity_and_abc(self):
        """
        Test that Person class is instance and subclass of entity and ABC

        """
        for parents in [Person, ABC]:
            isinstance(self.person, parents)
            issubclass(self.person.__class__, parents)

    def test_can_access_method_set_age(self):
        """
        Test that it is possible to access the method set_age() method

        """
        assert self.person.sifo_age(18) == '19'

    @pt.mark.parametrize('age', [18, 18.0, '18', '18.0', 'test', (), [], {}])
    def test_set_age_with_different_data_types(self, age):
        """
        Test that set_age() method accepts only (int, float, str)

        """
        try:
            assert self.person.sifo_age(age) == '19'
        except TrackingError:
            with pt.raises(TrackingError):
                self.person.sifo_age(age)

    @pt.mark.parametrize('negative_age', [-18, -18.0, '-18', '-18.0'])
    def test_only_non_negative_numbers_accepted(self, negative_age):
        """
        Test only non-negative numbers can be passed to the set_age() method

        """
        with pt.raises(TrackingError):
            self.person.sifo_age(negative_age)

    @pt.mark.parametrize('yrs', [0.41, 0.91, 1, 2, 3, 5, 9, 13, 17, 19, 50, 60, 66, 75])
    def test_sifo_age_corner_cases(self, yrs):
        """
        Test all corner cases of set_age() method

        """
        for limit in [yrs - 0.05, yrs]:
            assert self.person.sifo_age(limit) == str(yrs)
