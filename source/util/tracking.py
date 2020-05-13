# -*- coding: utf-8 -*-
"""
Module containing decorator for tracking and logging exceptions

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from functools import update_wrapper

from .exceptions import TrackingError
from .logging import LOGGER


class Tracking:
    """
    Tracking decorator

    """

    def __init__(self, func, type_=None):
        """
        Constructor / Instantiate the class

        """
        self.func = func
        self.type = type_
        self.argument = True
        update_wrapper(self, self.func)

    def __get__(self, obj, type_=None):
        """
        private get method

        """
        func = self.func.__get__(obj, type_)
        return self.__class__(func, type_)

    def __call__(self, *args, **kwargs):
        """
        private call method

        """
        try:
            function = self.func(*args, **kwargs)
            return function
        except Exception as tracking_exception:
            if self.func.__name__ == "__init__":
                msg = "[{}] -> '{}'".format(self.type.__name__, tracking_exception)
            else:
                msg = "[{}.{}] -> '{}'".format(self.type.__name__,
                                               self.func.__name__, tracking_exception)
            LOGGER.exception(msg)
            raise TrackingError(msg)
