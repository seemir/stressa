# -*- coding: utf-8 -*-

"""
Stressa settings file

This file contains important constants, including url, db connection strings and credentials

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

FINN_URL = "https://www.finn.no/realestate/homes/ad.html?finnkode="

PORTALEN_URL = "https://www.finansportalen.no/feed/v3/bank/boliglan.atom"
PORTALEN_CRED = tuple(os.environ.get(cred) for cred in ["PORTALEN_USERNAME", "PORTALEN_PASSWORD"])
PORTALEN_ENTRY = "{http://www.w3.org/2005/Atom}entry"

SIFO_URL = "http://kalkulator.referansebudsjett.no/php/blank_template.php"
SIFO_FORM = "budsjett"

POSTEN_URL = "https://adressesok.posten.no/nb/postal_codes/search"
POSTEN_FORM = "q"

SSB_URL = "https://data.ssb.no/api/v0/no/table/10748"
