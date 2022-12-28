# -*- coding: utf-8 -*-

"""
All workflow logic are stored in this subpackage

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from .finn_transportation_process import FinnTransportationProcess
from .skatteetaten_tax_processing import SkatteetatenTaxProcessing
from .finn_family_data_processing import FinnFamilyDataProcessing
from .finn_people_data_processing import FinnPeopleDataProcessing
from .mortgage_analysis_process import MortgageAnalysisProcess
from .finn_environment_process import FinnEnvironmentProcess
from .skattetaten_tax_parsing import SkatteetatenTaxParsing
from .finn_leisure_processing import FinnLeisureProcessing
from .finn_shopping_sub_model import FinnShoppingSubModel
from .finn_advert_processing import FinnAdvertProcessing
from .finn_community_process import FinnCommunityProcess
from .sifo_expenses_process import SifoExpensesProcess
from .finn_shopping_process import FinnShoppingProcess
from .restructure_process import RestructureProcess
from .postal_code_process import PostalCodeProcess

from .engine import *
