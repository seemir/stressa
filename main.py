# -*- coding: windows-1252 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.api import SsbInterestRates, ZipCodeFinder, SifoExpenses, SsbPayload
from source.domain import Female, Family, Male

father = Male(age=45)
mother = Female(age=40)
girl = Female(age=13, sfo='1')
boy = Male(age=10, sfo='1')

family = Family([father, mother, girl, boy], income=850000, cars=2)

family.sifo_properties()

sifo = SifoExpenses(family)
sifo.to_json()

posten = ZipCodeFinder('6239')
posten.to_json()

payload = SsbPayload()
ssb = SsbInterestRates(payload)
ssb.to_json()
