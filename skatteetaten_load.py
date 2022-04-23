# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import json

from source.app import SkatteetatenTaxProcessing

tax_form = {"skatte_aar": 2022, "brutto_inntekt_total": 671000, "alder": 32,
            "fagforeningskontigent": 2250, "bsu": 25000, "rentekostnader_total": 11500,
            "renteinntekter_total": 15000}

tax_data = SkatteetatenTaxProcessing(tax_form)

with open('skatteetaten.json', 'w') as fp:
    json.dump(tax_data.skatteetaten_tax_info, fp, indent=4)
