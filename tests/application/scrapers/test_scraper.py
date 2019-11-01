# -*- coding: utf-8 -*-

"""
Test module for all Scraper tests

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import shutil
import json
import os

import pytest as pt

from source.application import Scraper


class TestScraper:
    """
    Test case for Scraper abstract base clas

    """

    @staticmethod
    def test_scraper_base_class_cannot_be_instantiated():
        """
        Test that scraper base class cannot be instantiated

        """
        with pt.raises(TypeError):
            Scraper()

    @staticmethod
    @pt.mark.parametrize("file_object", [{"foo": "bar"}, {"hello": "world"}])
    def test_static_to_json_method(file_object):
        """
        Test that staticmethod _to_json() produces json file with correct content

        """
        file_dir = os.path.dirname(__file__) + "report/"
        Scraper.save_json(file_object, file_dir=file_dir)
        with open(file_dir + os.listdir(file_dir)[-1]) as json_file:
            data = json.load(json_file)
        assert data == file_object
        shutil.rmtree(file_dir, ignore_errors=True)

    @staticmethod
    @pt.mark.parametrize("invalid_file_dir", ["////"])
    @pt.mark.parametrize("file_object", [{"foo": "bar"}, {"hello": "world"}])
    def test_to_json_raises_os_error_for_invalid_dir(file_object, invalid_file_dir):
        """
        Test that _to_json() throws OSError if file_dir is invalid

        """
        with pt.raises(OSError):
            Scraper.save_json(file_object, file_dir=invalid_file_dir)
