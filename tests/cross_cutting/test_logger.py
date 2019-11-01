# -*- coding: utf-8 -*-

"""
Test module for logging function

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from loguru import logger
import pytest as pt

from source.cross_cutting import logging


class TestLogger:
    """
    Test cases for logging function

    """

    @staticmethod
    def test_logger_produces_loguru_logger():
        """
        Test that all loggr outputs are instances of loguru logger

        """
        assert isinstance(logging(), logger.__class__)

    @staticmethod
    def test_logger_throws_os_error_for_invalid_file_path():
        """
        Test that logr throws OSError for invalid file path

        """
        with pt.raises(OSError):
            logging(file_path="////")  # invalid file_path
