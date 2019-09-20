# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.domain.person import Person
from source.domain.female import Female
from source.domain.male import Male
import pytest as pt


class TestMaleAndFemale:

    def test_male_and_female_are_instances_and_subclasses_of_person(self):
        """
        Test that all Male and Female instances are subclass and instance of Person superclass

        """
        for person in [Male(), Female()]:
            assert isinstance(person, Person)
            assert issubclass(person.__class__, Person)
