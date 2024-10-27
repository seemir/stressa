# -*- coding: utf-8 -*-
"""
Module containing decorator for debugging and logging exceptions

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from .tracking import Tracking
from .logging import LOGGER


class Debugger(Tracking):
    """
    Debugging decorator

    """

    def __call__(self, *args, **kwargs):
        """
        private call method

        """
        try:
            function = self.func(*args, **kwargs)
            return function
        except Exception as debugger_exception:
            if self.func.__name__ == "__init__":
                msg = f"[{self.type.__name__}] -> '{debugger_exception}'"
            else:
                msg = f"[{self.type.__name__}.{self.func.__name__}] -> '{debugger_exception}'"
            LOGGER.debug(msg)
