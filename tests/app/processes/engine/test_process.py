# -*- coding: utf-8 -*-
"""
Test module for the Process class

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from abc import ABC

from prettytable import PrettyTable
from pydot import Dot
import pytest as pt

from source.app import Process


class TestProcess:
    """
    Test cases for the Process class

    """

    @staticmethod
    def test_process_is_instance_and_subclass_of_dot_and_abc():
        """
        Test that Process is an instance and subclass of Process, Dot and ABC

        """
        for parent in [Process, Dot, ABC]:
            assert issubclass(Process, parent)

    @staticmethod
    def test_process_cannot_be_instantiated():
        """
        Test that Process cannot be instantiated as it is an Abstract Base Class

        """
        with pt.raises(TypeError):
            Process("test_process")

    @staticmethod
    def test_process_class_variables():
        """
        Test that Process class variables profiling and start are None

        """
        assert not Process.profiling
        assert not Process.start

    @staticmethod
    def test_start_process_class_method():
        """
        Test the Process start_process() method

        """
        Process.start_process()
        assert isinstance(Process.start, float)
        assert isinstance(Process.profiling.__class__, PrettyTable.__class__)

    @staticmethod
    def test_end_process_class_method():
        """
        Test the Process end_process() method

        """
        Process.start_process()
        start_profiling = str(Process.profiling)
        Process.end_process()
        end_profiling = str(Process.profiling)

        assert "total" not in start_profiling
        assert "total" in end_profiling
