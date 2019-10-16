# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.log import main_logger

# disable logging whe running tests
main_logger.remove()
