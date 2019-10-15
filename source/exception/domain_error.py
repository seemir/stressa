# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'


class DomainError(Exception):
    """
    Exception thrown when breach of logic in domain object

    """

    def __init__(self, msg: str):
        self.msg = msg
