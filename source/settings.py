# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

sifo_url = "http://kalkulator.referansebudsjett.no/php/blank_template.php"
sifo_form = "budsjett"

posten_url = "https://adressesok.posten.no/en/postal_codes/search"
posten_form = "q"

ssb_url = "https://data.ssb.no/api/v0/no/table/10748"

portalen_url = "https://www.finansportalen.no/feed/v3/bank/boliglan.atom"
portalen_cred = tuple(os.environ.get(cred) for cred in ["PORTALEN_USERNAME", "PORTALEN_PASSWORD"])
portalen_entry = "{http://www.w3.org/2005/Atom}entry"

db_cred = tuple(os.environ.get(cred) for cred in ["DB_USERNAME", "DB_PASSWORD"])
db_string = os.environ.get("DB_CONNECTION").format(db_cred[0], db_cred[1], db_cred[0][:-3].lower())
