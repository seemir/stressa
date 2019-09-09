# -*- coding: windows-1252 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.api.ssb.ssb_interest_rates import SsbInterestRates
from source.api.posten.zip_code_finder import ZipCodeFinder
from source.api.sifo.sifo_expenses import SifoExpenses
from source.api.ssb.ssb_payload import SsbPayload
from source.domain.female import Female
from source.domain.family import Family
from source.domain.male import Male

father = Male(age=45)
mother = Female(age=40)
girl = Female(age=13, sfo='1')
boy = Male(age=10, sfo='1')

family = Family([father, mother, girl, boy], income=850000, cars=2)

sifo = SifoExpenses(family)
sifo.to_json()

posten = ZipCodeFinder('6239')
posten.to_json()

payload = SsbPayload()
ssb = SsbInterestRates(payload)
ssb.to_json()
