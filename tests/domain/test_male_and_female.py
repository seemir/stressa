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

    def test_male_and_female_have_correct_gender(self):
        """
        Test that Male and Female objects have correct gender classification

        """
        persons = {'m': Male(), 'k': Female()}
        for gender, person in persons.items():
            assert person.kjonn == gender

    @pt.mark.parametrize('invalid_age', [(), [], {}])
    def test_type_checking_person_input_arguments(self, invalid_age):
        """
        Test that TypeError is raised if invalid arg for age, kinder_garden or sfo is passed
        to person (Male or Female) object.

        """
        persons = [Male(), Female()]
        for person in persons:
            with pt.raises(TypeError):
                person.alder = invalid_age
            with pt.raises(TypeError):
                person.barnehage = invalid_age
            with pt.raises(TypeError):
                person.sfo = invalid_age

    @pt.mark.parametrize('age', [0.42, 0.92, 1, 2, 3, 5, 9, 13, 17, 19, 50, 60, 66, 75])
    def test_person_attending_kinder_garden_or_sfo(self, age):
        """
        Test that only person of age between 1-5 can attend kinder_garden and person between
        6-13 can attend sfo. ValueError thrown if not the case.

        """
        persons = [Male(), Female()]
        kinder_garden = age in range(1, 6)
        sfo = age in range(6, 14)
        for person in persons:
            if kinder_garden:
                person.alder = age
                person.barnehage = '1'
                assert person.alder == str(age)
                assert person.barnehage == '1'
            elif sfo:
                person.alder = age
                person.sfo = '1'
                assert person.alder == str(age)
                assert person.sfo == '1'
            else:
                with pt.raises(ValueError):
                    person.__class__(age, kinder_garden='1')
                with pt.raises(ValueError):
                    person.__class__(age, sfo='1')

    @pt.mark.parametrize('age', [0.42, 0.92, 1, 2, 3, 5, 9, 13, 17, 19, 50, 60, 66, 75])
    def test_female_pregnancy(self, age):
        """
        Test that females can be pregnant only at ages between 19-50 years

        """
        female = Female()
        pregnancy = age in range(19, 51)
        if pregnancy:
            female.alder = age
            female.gravid = '1'
            assert female.alder == str(age)
            assert female.gravid == '1'
        else:
            with pt.raises(ValueError):
                female.__class__(age, pregnant='1')
