# -*- coding: utf-8 -*-
"""
init module for accessing chart types

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pyqtgraph as pg

from .bar_chart_with_line import BarChartWithLine
from .double_cross_hair import DoubleCrossHair
from .ratio_chart import RatioChart
from .bar_chart import BarChart

pg.setConfigOption('background', 'w')
