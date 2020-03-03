# -*- coding: utf-8 -*-
"""
module containing the logic for the chart abstract base class

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from abc import abstractmethod
from itertools import chain

import numpy as np
from pyqtgraph import PlotWidget
from PyQt5.QtCore import QObject

from source.util import Assertor


class Chart(QObject):
    """
    Chart abstract base class

    """

    @abstractmethod
    def __init__(self):
        """
        Constructor / Instantiation of class

        """
        super().__init__(parent=None)
        self.name = self.__class__.__name__

    @staticmethod
    def clear_graphics(graphics_view: PlotWidget):
        """
        static method for clearing content in all graphics

        Parameters
        ----------
        graphics_view   : PlotWidget
                          graphics view to place chart

        """
        Assertor.assert_data_types([graphics_view], [PlotWidget])
        graphics_view.clear()

    @staticmethod
    def create_bins(x: list, y: list, bins: list):
        """
        method for creating bins for bar char

        Parameters
        ----------
        x       : list
                  x-values
        y       : list
                  y-value
        bins    : list
                  bins

        Returns
        -------
        out     : np.ndarray
                  bins for bar chart

        """
        Assertor.assert_data_types([x, y, bins], [list, list, list])
        bin_array = []
        for i, value in enumerate(x):
            if y[i] != 0:
                bin_array.append([value] * y[i])
            else:
                bin_array.append([0])
        return np.histogram(list(chain(*bin_array)), bins=bins)
