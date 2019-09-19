# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.domain.person import Person
from source.domain.female import Female
from source.domain.male import Male
import pytest as pt


def test_all_people_are_subclass_and_instance_of_person():
    """
    Test that all Male and Female instances are subclass and instance of Person superclass

    """
    for person in [Male(), Female()]:
        assert isinstance(person, Person)
        assert isinstance(person, (Male, Female))
        assert issubclass(person.__class__, Person)


@pt.mark.parametrize('kjonn', ['m', 'k'])
@pt.mark.parametrize('alder', [0.42, 0.92, 1, 75])
@pt.mark.parametrize('barnehage', ['0', '1'])
@pt.mark.parametrize('sfo', ['0', '1', '2'])
@pt.mark.parametrize('gravid', ['0', '1'])
class TestPeople:

    @pt.mark.parametrize('invalid_arg', ['test', (), [], {}])
    def test_invalid_arguments_raises_type_error(self, invalid_arg, kjonn, alder, barnehage, sfo,
                                                 gravid):
        """
        Test that TypeError is raised when invalid arguments are passed through
        Male and Female constructor

        """
        for person in [Male, Female]:
            with pt.raises(TypeError):
                person(sex=invalid_arg, age=alder, kinder_garden=barnehage, sfo=sfo,
                       pregnant=gravid)
            with pt.raises(TypeError):
                person(sex=kjonn, age=invalid_arg, kinder_garden=barnehage, sfo=sfo,
                       pregnant=gravid)
            with pt.raises(TypeError):
                person(sex=kjonn, age=alder, kinder_garden=invalid_arg, sfo=sfo,
                       pregnant=gravid)
            with pt.raises(TypeError):
                person(sex=kjonn, age=alder, kinder_garden=barnehage, sfo=invalid_arg,
                       pregnant=gravid)
            with pt.raises(TypeError):
                person(sex=kjonn, age=alder, kinder_garden=barnehage, sfo=sfo,
                       pregnant=invalid_arg)

    def test_arguments_get_set_in_object_for_valid_arguments(self, kjonn, alder, barnehage, sfo,
                                                             gravid):
        """
        Test that arguments gets set in object, ValueError is thrown if not

        """
        try:
            prop = locals()
            del prop['self']
            prop['alder'] = str(prop['alder'])

            if kjonn == 'm':
                pers = Male()
                del prop['gravid']
            else:
                pers = Female()

            for name, value in prop.items():
                if name != 'kjonn':
                    setattr(pers, name, value)
                    assert getattr(pers, name) == value
                else:
                    assert getattr(pers, name) == value

        except ValueError:
            pass
