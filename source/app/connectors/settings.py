# -*- coding: utf-8 -*-

"""
Stressa settings file

This file contains constants, including url and credentials

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

FINN_AD_URL = "https://finn.no/realestate/homes/ad.html?finnkode="
FINN_OWNER_URL = "https://finn.no/realestate/ownershiphistory.html?finnkode="
FINN_STAT_URL = "https://www.finn.no/prisstatistikk/"
FINN_COMMUNITY_URL = "https://profil.nabolag.no/"

PORTALEN_URL = "https://www.finansportalen.no/services/feed/v3/bank/boliglan.atom"
PORTALEN_CRED = tuple(os.environ.get(cred) for cred in ["PORTALEN_USERNAME", "PORTALEN_PASSWORD"])
PORTALEN_ENTRY = "{http://www.w3.org/2005/Atom}entry"

POSTEN_URL = "https://adressesok.posten.no/api/v1/postal_codes.json?postal_code="

SIFO_URL = "https://kalkulator.referansebudsjett.no/php/resultat_as_json.php?"

SSB_URL = "https://data.ssb.no/api/v0/no/table/10748"

SKATTEETATEN_URL = "https://skatteberegning.app.skatteetaten.no/"

TIMEOUT = 15
