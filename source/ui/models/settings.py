# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

FINN_URL = 'https://www.finn.no/realestate/browse.html'

_lanetype = ["", "Sammenligning", "Annuitetslån", "Serielån"]
_laneperiode = [""] + [str(yr) + " år" for yr in range(1, 31)],
_interval = ["", "Ukentlig", "Annenhver uke", "Månedlig", "Annenhver måned",
             "Kvartalsvis", "Årlig"]
