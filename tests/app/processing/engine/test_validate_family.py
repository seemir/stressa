# -*- coding: utf-8 -*-
"""
Test module for the validate family operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from source.app import ValidateFamily, Operation
from source.domain import Family


class TestValidateFamily:
    """
    Test cases for the ValidateFamily operation

    """

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.data = {"person_1": {"alder_1": "20-50", "kjonn_1": "Mann"},
                    "person_2": {"alder_2": "20-50", "gravid_2": "Ja", "kjonn_2": "Kvinne"},
                    "person_3": {"alder_3": "6-9", "kjonn_3": "Kvinne", "sfo_3": "Heldag"},
                    "person_4": {"alder_4": "3", "barnehage_4": "Ja", "kjonn_4": "Mann"},
                    "antall_biler": "1", "brutto_arsinntekt": "1 260 000 kr"}

    def test_validate_family_is_instance_of_operation(self):
        """
        Test that validate_family is instance and subclass of Operation

        """
        validate = ValidateFamily(self.data)
        for parent in [ValidateFamily, Operation]:
            assert isinstance(validate, parent)
            assert issubclass(validate.__class__, parent)

    @staticmethod
    def test_class_variables():
        """
        Test that all the class variables are correct in the object

        """
        sfo_arg = {"Nei": "0", "Halvdag": "1", "Heldag": "2"}
        barnehage_arg = {"Nei": "0", "Ja": "1"}
        sifo_age = {"0-5 mnd": 0.41, "6-11 mnd": 0.91, "1": 1, "2": 2, "3": 3, "4-5": 5,
                    "6-9": 9, "10-13": 13, "14-17": 17, "18-19": 19, "20-50": 50, "51-60": 60,
                    "61-66": 66, "eldre enn 66": 75}

        assert ValidateFamily.sifo_arg == sifo_age
        assert ValidateFamily.barnehage_arg == barnehage_arg
        assert ValidateFamily.sfo_arg == sfo_arg

    @staticmethod
    @pt.mark.parametrize('invalid_data', [True, 'test', 90210, 90210.0, ('test', 'test')])
    def test_invalid_args_raises_typeerror(invalid_data):
        """
        Test that validate_family object raises TypeError if data is invalid

        """
        with pt.raises(TypeError):
            ValidateFamily(invalid_data)

    def test_arguments_gets_set_in_object(self):
        """
        Test that arguments gets set in the ValidateFamily object

        """
        validate = ValidateFamily(self.data)
        assert validate.name == ValidateFamily.__name__
        assert validate.data == self.data

    def test_validate_family_run_method(self):
        """
        Test that the run method returns Family object

        """
        validate = ValidateFamily(self.data)
        assert isinstance(validate.run(), Family)
        assert issubclass(validate.run().__class__, Family)
