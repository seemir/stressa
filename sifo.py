# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import mechanize

br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_refresh(False)
br.open('http://kalkulator.referansebudsjett.no/php/blank_template.php')
br.select_form(name="budsjett")

