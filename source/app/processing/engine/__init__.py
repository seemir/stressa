# -*- coding: utf-8 -*-
"""
Workflow engine for controlling and documenting all calculations in application

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from .scrape_sifo_base_expenses import ScrapeSifoBaseExpenses
from .scrape_finn_ownership_history import ScrapeFinnOwnershipHistory
from .scrape_finn_stat_info import ScrapeFinnStatisticsInfo
from .scrape_finn_ad_info import ScrapeFinnAdInfo
from .validate_finn_code import ValidateFinnCode
from .output_operation import OutputOperation
from .validate_family import ValidateFamily
from .input_operation import InputOperation
from .output_signal import OutputSignal
from .operation import Operation
from .muliplex import Multiplex
from .process import Process
from .extract import Extract
from .signal import Signal
from .divide import Divide
