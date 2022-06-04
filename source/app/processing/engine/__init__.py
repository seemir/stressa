# -*- coding: utf-8 -*-
"""
Workflow engine for controlling and documenting all calculations in application

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from .finn_community_statistics_connector import FinnCommunityStatisticsConnector
from .finn_ownership_history_connector import FinnOwnershipHistoryConnector
from .skatteetaten_tax_info_connector import SkatteetatenTaxInfoConnector
from .finn_statistics_info_connector import FinnStatisticsInfoConnector
from .sifo_base_expenses_connector import SifoBaseExpensesConnector
from .finn_advert_info_connector import FinnAdvertInfoConnector
from .postal_code_info_connector import PostalCodeInfoConnector
from .validate_postal_code import ValidatePostalCode
from .restructure_ratings import RestructureRatings
from .add_row_to_dataframe import AddRowToDataFrame
from .validate_finn_code import ValidateFinnCode
from .validate_mortgage import ValidateMortgage
from .restructure_score import RestructureScore
from .extract_first_row import ExtractFirstRow
from .check_newest_date import CheckNewestDate
from .validate_tax_form import ValidateTaxForm
from .output_operation import OutputOperation
from .restructure_pois import RestructurePois
from .validate_family import ValidateFamily
from .input_operation import InputOperation
from .multiplication import Multiplication
from .rate_of_change import RateOfChange
from .output_signal import OutputSignal
from .restructure import Restructure
from .subtraction import Subtraction
from .accumulate import Accumulate
from .operation import Operation
from .multiplex import Multiplex
from .sub_model import SubModel
from .addition import Addition
from .separate import Separate
from .division import Division
from .process import Process
from .extract import Extract
from .flatten import Flatten
from .signal import Signal
from .factor import Factor
