# -*- coding: utf-8 -*-

"""
Test module for all Connector tests

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import shutil
import json
import os

import pytest as pt

from source.app import Connector


class TestConnector:
    """
    Test case for Connector abstract base class

    """

    @staticmethod
    def test_connector_base_class_cannot_be_instantiated():
        """
        Test that connector base class cannot be instantiated

        """
        with pt.raises(TypeError):
            Connector()

    @staticmethod
    @pt.mark.parametrize("file_content", [{"foo": "bar"}])
    def test_static_save_json_method(file_content):
        """
        Test that staticmethod save_json() produces json file with correct content

        """
        current_dir = os.path.dirname(__file__)
        file_dir = os.path.join(current_dir, "report", "json")
        Connector.save_json(file_content, file_dir=file_dir)
        with open(os.path.join(file_dir, os.listdir(file_dir)[-1])) as json_file:
            data = json.load(json_file)
            assert data == file_content
        shutil.rmtree(os.path.join(current_dir, "report"), ignore_errors=True)

    @staticmethod
    @pt.mark.parametrize("invalid_file_dir", ["////"])
    @pt.mark.parametrize("file_object", [{"foo": "bar"}, {"hello": "world"}])
    def test_save_json_raises_os_error_for_invalid_dir(file_object, invalid_file_dir):
        """
        Test that save_json() throws OSError if file_dir is invalid

        """
        with pt.raises(OSError):
            Connector.save_json(file_object, file_dir=invalid_file_dir)
