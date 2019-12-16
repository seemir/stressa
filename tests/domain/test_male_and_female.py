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

    @staticmethod
    def test_male_and_female_are_instances_and_subclasses_of_person_entity():
        """
        Test that all Male and Female instances are subclass and instance of
        Person and Entity classes

        """
        for person in [Male(), Female()]:
            for parents in [Person, Entity]:
                assert isinstance(person, parents)
                assert issubclass(person.__class__, parents)

    @staticmethod
    def test_male_and_female_have_correct_gender():
        """
        Test that Male and Female objects have correct gender classification

        """
        persons = {'m': Male(), 'k': Female()}
        for gender, person in persons.items():
            assert person.kjonn == gender

    @staticmethod
    @pt.mark.parametrize('invalid_age', [(), [], {}])
    def test_type_checking_person_input_arguments(invalid_age):
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

    @staticmethod
    @pt.mark.parametrize('age', [0.41, 0.91, 1, 2, 3, 5, 9, 13, 17, 19, 50, 60, 66, 75])
    def test_person_attending_kinder_garden_or_sfo(age):
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

    @staticmethod
    @pt.mark.parametrize('age', [0.41, 0.91, 1, 2, 3, 5, 9, 13, 17, 19, 50, 60, 66, 75])
    def test_female_pregnancy(age):
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

    @staticmethod
    def test_male_and_female_id_are_uuid4():
        """
        Test that Male and Female entity class ids are uuid4 compatible

        """
        for person in [Male(), Female()]:
            assert UUID(str(person.id_str))
