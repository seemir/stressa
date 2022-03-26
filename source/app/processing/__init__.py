# -*- coding: utf-8 -*-

"""
All workflow logic are stored in this subpackage

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from .posten_postal_code_extraction import PostenPostalCodeExtraction
from .finn_transportation_process import FinnTransportationProcess
from .skatteetaten_tax_processing import SkatteetatenTaxProcessing
from .finn_family_data_processing import FinnFamilyDataProcessing
from .finn_people_data_processing import FinnPeopleDataProcessing
from .finn_environment_process import FinnEnvironmentProcess
from .finn_leisure_processing import FinnLeisureProcessing
from .finn_shopping_sub_model import FinnShoppingSubModel
from .finn_advert_processing import FinnAdvertProcessing
from .finn_community_process import FinnCommunityProcess
from .sifo_expenses_process import SifoExpensesProcess
from .finn_shopping_process import FinnShoppingProcess
from .engine import *
