# -*- coding: utf-8 -*-
"""
Module containing utilises for profiling processes

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from time import time
from datetime import datetime

from prettytable import PrettyTable, NONE


class Profiling:
    """
    Process profiling decorator

    """

    def __init__(self, func, type_=None):
        """
        Constructor / Instantiate the class

        """
        self.func = func
        self.type = type_

    def __get__(self, obj, type_=None):
        func = self.func.__get__(obj, type_)
        return self.__class__(func, type_)

    def __call__(self, *args, **kwargs):
        start = time()
        function = self.func(*args, **kwargs)
        end = time()
        self.type.profiling.add_row(
            [self.func.__name__, self.local_time(start), self.local_time(end),
             str(round((end - start) * 1000, 7)) + "ms"])
        return function

    @staticmethod
    def local_time(sec):
        """
        method for getting local time in isoformat from secs

        Parameters
        ----------
        sec     : float
                  seconds from epoch

        Returns
        -------
        out     : datetime
                  isoformated date

        """
        return datetime.fromtimestamp(sec).isoformat()


def profiling_config():
    """
    basic configuration for profiling table

    Returns
    -------
    out        : PrettyTable
                 profiling configuration

    """
    profiling_table = PrettyTable(hrules=NONE, vrules=NONE)
    profiling_table.field_names = ["operation", "start", "end", "elapsed"]
    profiling_table.align = "l"
    profiling_table.align["elapsed"] = "r"
    profiling_table.add_row(["---------" for _ in range(4)])
    return profiling_table
