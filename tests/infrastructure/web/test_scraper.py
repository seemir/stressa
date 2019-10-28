# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.exception import InstantiationError
from source.infrastructure import Scraper
import pytest as pt
import shutil
import json
import os


class TestScraper:

    def test_scraper_base_class_cannot_be_instantiated(self):
        """
        Test that scraper base class cannot be instantiated

        """
        with pt.raises(InstantiationError):
            Scraper()

    @pt.mark.parametrize("file_dir", ["report"])
    @pt.mark.parametrize("file_object", [{"foo": "bar"}, {"hello": "world"}])
    def test_static_to_json_method(self, file_object, file_dir):
        """
        Test that staticmethod _to_json() produces json file with correct content

        """
        Scraper._to_json(file_object, file_dir=file_dir)
        with open(file_dir + '/' + os.listdir(file_dir)[-1]) as json_file:
            data = json.load(json_file)
        assert data == file_object
        shutil.rmtree(file_dir, ignore_errors=True)

    @pt.mark.parametrize("invalid_file_dir", ["////"])
    @pt.mark.parametrize("file_object", [{"foo": "bar"}, {"hello": "world"}])
    def test_to_json_raises_os_error_for_invalid_dir(self, file_object, invalid_file_dir):
        """
        Test that _to_json() throws OSError if file_dir is invalid

        """
        with pt.raises(OSError):
            Scraper._to_json(file_object, file_dir=invalid_file_dir)
