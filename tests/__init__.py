# -*- coding: utf-8 -*-

"""
Application test package

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.log import LOGGER

# remove main logger when running tests
LOGGER.remove()
