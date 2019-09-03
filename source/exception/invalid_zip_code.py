# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'


class InvalidZipCode(Exception):
    """
    Exception when zip-code not found

    """

    def __init__(self, msg):
        self.msg = msg
