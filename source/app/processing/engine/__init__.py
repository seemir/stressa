# -*- coding: utf-8 -*-
"""
Workflow engine for controlling and documenting all calculations in application

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from .scrape_finn_ownership_history import ScrapeFinnOwnershipHistory
from .scrape_sifo_base_expenses import ScrapeSifoBaseExpenses
from .scrape_finn_statistics_info import ScrapeFinnStatisticsInfo
from .scrape_finn_advert_info import ScrapeFinnAdvertInfo
from .add_row_to_dataframe import AddRowToDataFrame
from .validate_finn_code import ValidateFinnCode
from .extract_first_row import ExtractFirstRow
from .check_newest_date import CheckNewestDate
from .output_operation import OutputOperation
from .validate_family import ValidateFamily
from .input_operation import InputOperation
from .output_signal import OutputSignal
from .price_change import PriceChange
from .operation import Operation
from .muliplex import Multiplex
from .process import Process
from .extract import Extract
from .signal import Signal
from .divide import Divide
