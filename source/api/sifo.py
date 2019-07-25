# -*- coding: windows-1252 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import xml.etree.ElementTree as Et
from mechanize import Browser
from bs4 import BeautifulSoup
import json

browser = Browser()
browser.set_handle_robots(False)
browser.set_handle_refresh(False)

browser.open('http://kalkulator.referansebudsjett.no/php/blank_template.php')
browser.select_form('budsjett')
browser["kjonn0"] = ['m']
browser["alder0"] = ['50']
browser["inntekt"] = '350000'
br_response = browser.submit()

soup = BeautifulSoup(br_response, "xml").prettify()
root = Et.fromstring(soup)

expenses = {}
for child in root:
    expenses.update({child.tag: child.text.strip().replace(".", "")})

print(expenses)

js = json.dumps(expenses, indent=3, separators=(',', ': '), ensure_ascii=False)
print(js)
with open('expenses.json', 'w') as f:
    f.write(js)
