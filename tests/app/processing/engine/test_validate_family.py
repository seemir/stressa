# -*- coding: utf-8 -*-
"""
Test module for the validate family operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from source.app import ValidateFamily, Operation
from source.util import TrackingError
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
        cls.data = {"person_1": {"alder_1": "20-30 år", "kjonn_1": "Mann"},
                    "person_2": {"alder_2": "20-30 år", "gravid_2": "Ja", "kjonn_2": "Kvinne"},
                    "person_3": {"alder_3": "6-9 år", "kjonn_3": "Kvinne", "sfo_3": "Heldag"},
                    "person_4": {"alder_4": "3 år", "barnehage_4": "Ja", "kjonn_4": "Mann"},
                    "antall_biler": "1", "brutto_arsinntekt": "1 260 000 kr", "select_year": "2021"}

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
        sifo_age = {'0-5 mnd': 0.41, '1 år': 1, '10-13 år': 13, '14-17 år': 17, '18-19 år': 19,
                    '2 år': 2, '20-30 år': 30, '3 år': 3, '31-50 år': 50, '4-5 år': 5,
                    '51-60 år': 60, '6-11 mnd': 0.91, '6-9 år': 9, '61-66 år': 66, '67-73 år': 74,
                    'eldre enn 74 år': 999}

        assert ValidateFamily.sifo_arg == sifo_age
        assert ValidateFamily.bool_arg == barnehage_arg
        assert ValidateFamily.sfo_arg == sfo_arg

    @staticmethod
    @pt.mark.parametrize('invalid_data', [True, 'test', 90210, 90210.0, ('test', 'test')])
    def test_invalid_args_raises_tracking_error(invalid_data):
        """
        Test that validate_family object raises TrackingError if data is invalid

        """
        with pt.raises(TrackingError):
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
