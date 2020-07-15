# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

from diagrams.custom import Custom

from source.util import __version__

name = "Stressa v." + __version__
font_size = "16"

icons = os.path.dirname(os.path.abspath(__file__)) + "\\icons\\"
ssb_logo = icons + "ssb_logo.png"
finn_logo = icons + "finn_logo.png"
posten_logo = icons + "posten_logo.png"
sifo_logo = icons + "sifo_logo.png"
finansportalen_logo = icons + "finansportalen_logo.png"
sqlite_logo = icons + "sqlite_logo.png"


class Finansportalen(Custom):
    def __init__(self, label):
        super().__init__(label=label, icon_path=finansportalen_logo)


class Finn(Custom):
    def __init__(self, label):
        super().__init__(label=label, icon_path=finn_logo)


class Posten(Custom):
    def __init__(self, label):
        super().__init__(label=label, icon_path=posten_logo)


class SIFO(Custom):
    def __init__(self, label):
        super().__init__(label=label, icon_path=sifo_logo)


class Sqlite(Custom):
    def __init__(self, label):
        super().__init__(label=label, icon_path=sqlite_logo)


class SSB(Custom):
    def __init__(self, label):
        super().__init__(label=label, icon_path=ssb_logo)
