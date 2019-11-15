# -*- coding: utf-8 -*-

"""
Settings file for views

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

FINN_URL = 'https://www.finn.no/realestate/browse.html'

LINE_EDITS = {"zip_code": ["postnr", "poststed", "kommune", "fylke"],
              "finn_code": ["sistendret", "referanse", "finn_adresse", "prisantydning",
                            "formuesverdi", "fellesgjeld", "felleskostmnd", "omkostninger",
                            "kommunaleavg", "totalpris", "fellesformue", "boligtype", "eieform",
                            "etasje", "bygger", "soverom", "rom", "primrrom", "bruttoareal",
                            "energimerking", "tomteareal"]}

FIELDS = {"kjønn": ["", "Mann", "Kvinne"],
          "lånetype": ["", "Sammenligning", "Annuitetslån", "Serielån"],
          "låneperiode": [""] + [str(yr) + " år" for yr in range(1, 31)],
          "betalingsinterval": ["", "Ukentlig", "Annenhver uke", "Månedlig", "Annenhver måned",
                                "Kvartalsvis", "Årlig"]}
