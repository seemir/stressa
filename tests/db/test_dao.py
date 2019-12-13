# -*- coding: utf-8 -*-

"""
Test module for the Data Access Object class

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.db import Dao


class TestDao:
    """
    Test cases for the Data Access Object (DAO) implementation

    """

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.dao = Dao()

    def test_is_instance_of_dao(self):
        """
        Test that dao is instance and subclass of Dao

        """
        assert isinstance(self.dao, Dao)
        assert issubclass(self.dao.__class__, Dao)
