# -*- coding: utf-8 -*-

"""
Test module for Sifo scraper class

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from uuid import UUID

import pytest as pt
from mechanize._response import response_seek_wrapper

from source.infrastructure import Scraper, Sifo
from source.domain import Female, Family, Male


class TestSifo:
    """
    Test cases for Sifo scraper

    """

    @classmethod
    def setup(cls):
        """
        Executed before every test

        """
        family_members = [Male(age=45), Female(age=40), Female(age=13, sfo='1'),
                          Male(age=10, sfo='1')]
        cls.family = Family(family_members, income=850000, cars=2)
        cls.sifo = Sifo(cls.family)

    @staticmethod
    def test_sifo_is_instance_of_scraper():
        """
        Test that Sifo scraper is instance and subclass of Scraper

        """
        assert isinstance(Sifo, Scraper.__class__)
        assert issubclass(Sifo.__class__, Scraper.__class__)

    @staticmethod
    @pt.mark.parametrize("invalid_family", [90210, 90210.0, True, [], (), {}])
    def test_sifo_raises_type_error_if_family_instance_not_passed(invalid_family):
        """
        TypeError thrown if Sifo does not get passed a Family instance
        through constructor

        """
        with pt.raises(TypeError):
            Sifo(invalid_family)

    def test_sifo_has_uuid4_compatible_id(self):
        """
        Test sifo scraper has uuid4 compatible ids

        """
        assert UUID(str(self.sifo.id_str))

    def test_that_family_get_set(self):
        """
        Test that Family object gets set if passed through constructor or setter

        """
        assert self.sifo.family == self.family

        new_family = Family([Female(age=40), Female(age=13, sfo='1'), Male(age=10, sfo='1')])
        self.sifo.family = new_family
        assert self.sifo.family == new_family

    def test_response_received(self):
        """
        Test HTTP response 200 is received and of correct type, i.e. response_seek_wrapper

        """
        response = self.sifo.response()
        assert response.code == 200
        assert isinstance(response, response_seek_wrapper)
