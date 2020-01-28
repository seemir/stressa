# -*- coding: utf-8 -*-

"""
Test module for Cashing of requests

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
import shutil

import pytest as pt
import requests

from source.util import cache


class TestCaching:
    """
    Test cases for cache of requests

    """

    @staticmethod
    def test_cache_requests():
        """
        Test that requests gets cached

        """
        current_dir = os.path.dirname(__file__)
        file_dir = os.path.join(current_dir, "temp")
        cache(file_dir, "cache")
        requests.post("http://www.google.com", data={"foo": "bar"})
        assert os.path.exists(file_dir)
        assert os.path.isfile(file_dir + "/cache.sqlite")
        shutil.rmtree(os.path.join(current_dir, "temp"), ignore_errors=True)

    @staticmethod
    def test_invalid_file_path_throws_os_error():
        """
        Test that an invalid file_path throws OSError

        """
        with pt.raises(OSError):
            cache("////", "cache")
