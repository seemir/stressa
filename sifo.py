# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from mechanize import Browser
from bs4 import BeautifulSoup

browser = Browser()
browser.set_handle_robots(False)
browser.set_handle_refresh(False)

browser.open('http://kalkulator.referansebudsjett.no/php/blank_template.php')
browser.select_form('budsjett')
browser["kjonn0"] = ['m']
browser["alder0"] = ['50']
browser["inntekt"] = '350000'
br_response = browser.submit()

soup = BeautifulSoup(br_response, "html.parser")
print(soup.prettify())
