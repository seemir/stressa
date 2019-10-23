# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.settings import db_string
import pymongo

client = pymongo.MongoClient(db_string)

client.close()
