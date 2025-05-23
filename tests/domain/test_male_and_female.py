# -*- coding: utf-8 -*-

"""
Test module for both Male and Female entity classes

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from uuid import UUID
import pytest as pt

from source.domain import Entity, Person, Female, Male


class TestMaleAndFemale:
    """
    Test class for Male and Female entity classes

    """

    def setup_method(self):
        """
        Executed before all tests

        """
        self.persons = [Male(), Female()]

    def test_male_and_female_are_instances_and_subclasses_of_person_entity(self):
        """
        Test that all Male and Female instances are subclass and instance of
        Person and Entity classes

        """
        for person in self.persons:
            for parents in [Person, Entity]:
                assert isinstance(person, parents)
                assert issubclass(person.__class__, parents)

    def test_male_and_female_have_correct_gender(self):
        """
        Test that Male and Female objects have correct gender classification

        """
        persons = dict(zip(['m', 'k'], self.persons))
        for gender, person in persons.items():
            assert person.kjonn == gender

    @pt.mark.parametrize('invalid_age', [(), [], {}])
    def test_type_checking_person_input_arguments(self, invalid_age):
        """
        Test that TypeError is raised if invalid arg for age, kinder_garden or sfo is passed
        to person (Male or Female) object.

        """
        for person in self.persons:
            with pt.raises(TypeError):
                person.alder = invalid_age
            with pt.raises(TypeError):
                person.barnehage = invalid_age
            with pt.raises(TypeError):
                person.sfo = invalid_age

    @pt.mark.parametrize('age', [0.41, 0.91, 1, 2, 3, 5, 9, 13, 17, 19, 50, 60, 66, 75])
    def test_person_attending_kinder_garden_or_sfo(self, age):
        """
        Test that only person of age between 1-5 can attend kinder_garden and person between
        6-13 can attend sfo. ValueError thrown if not the case.

        """
        kinder_garden = age in range(1, 6)
        sfo = age in range(6, 14)
        for person in self.persons:
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

    @pt.mark.parametrize('age', [0.41, 0.91, 1, 2, 3, 5, 9, 13, 17, 19, 50, 60, 66, 75])
    def test_female_pregnancy(self, age):
        """
        Test that females can be pregnant only at ages between 19-50 years

        """
        female = self.persons[1]
        pregnancy = age in range(17, 51)
        if pregnancy:
            female.alder = age
            female.gravid = '1'
            assert female.alder == str(age)
            assert female.gravid == '1'
        else:
            with pt.raises(ValueError):
                female.__class__(age, pregnant='1')

    def test_male_and_female_id_are_uuid4(self):
        """
        Test that Male and Female entity class ids are uuid4 compatible

        """
        for person in self.persons:
            assert UUID(str(person.id_))
