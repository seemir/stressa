# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.log import loggr
from loguru import logger
import pytest as pt


class TestLoggr:

    def test_logr_produces_loguru_logger(self):
        """
        Test that all loggr outputs are instances of loguru logger

        """
        assert isinstance(loggr(), logger.__class__)

    def test_loggr_throws_os_error_for_invalid_file_path(self):
        """
        Test that logr throws OSError for invalid file path

        """
        with pt.raises(OSError):
            loggr(file_path="////")  # invalid file_path
