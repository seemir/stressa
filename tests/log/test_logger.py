# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.log import logging
from loguru import logger
import pytest as pt


class TestLogger:

    def test_logger_produces_loguru_logger(self):
        """
        Test that all loggr outputs are instances of loguru logger

        """
        assert isinstance(logging(), logger.__class__)

    def test_logger_throws_os_error_for_invalid_file_path(self):
        """
        Test that logr throws OSError for invalid file path

        """
        with pt.raises(OSError):
            logging(file_path="////")  # invalid file_path
