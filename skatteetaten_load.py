# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import json

from source.app import SkatteetatenTaxProcessing

tax_form = {"tax_year": 2022, "income": 671000, "age": 32}

tax_data = SkatteetatenTaxProcessing(tax_data=tax_form)

with open('skatteetaten.json', 'w') as fp:
    json.dump(tax_data.skatteetaten_tax_info, fp, indent=4)
