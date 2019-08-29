# -*- coding: windows-1252 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.domain.female import Female
from source.domain.family import Family
from source.domain.male import Male
from source.api.sifo import Sifo

father = Male(age=45)
mother = Female(age=40)
girl = Female(age=13, sfo='1')
boy = Male(age=10, sfo='1')

family = Family([father, mother, girl, boy], income=850000, cars=2)

sifo = Sifo(family)
sifo.to_json()
