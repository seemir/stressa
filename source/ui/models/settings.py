# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

LINE_EDITS = {"postnr": ["postnr",
                         "poststed",
                         "kommune",
                         "fylke"],
              "finn_kode": ["sistendret",
                            "referanse",
                            "finn_adresse",
                            "prisantydning",
                            "formuesverdi",
                            "fellesgjeld",
                            "felleskostmnd",
                            "omkostninger",
                            "kommunaleavg",
                            "totalpris",
                            "fellesformue",
                            "boligtype",
                            "eieform",
                            "etasje",
                            "bygger",
                            "soverom",
                            "rom",
                            "primrrom",
                            "bruttoareal",
                            "energimerking",
                            "tomteareal"],
              "navn": ["fornavn",
                       "etternavn"]}

FIELDS = {"kjønn": ["",
                    "Mann",
                    "Kvinne"],
          "lånetype": ["",
                       "Sammenligning",
                       "Annuitetslån",
                       "Serielån"],
          "låneperiode": [""] +
                         [str(yr) + " år" for yr in range(1, 31)],
          "interval": ["",
                       "Ukentlig",
                       "Annenhver uke",
                       "Månedlig",
                       "Annenhver måned",
                       "Kvartalsvis",
                       "Årlig"]}

FINN_URL = 'https://www.finn.no/realestate/browse.html'
