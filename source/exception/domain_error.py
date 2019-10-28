# -*- coding: utf-8 -*-

"""
Any Error within domain model throws DomainError exception

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'


class DomainError(Exception):
    """
    Exception thrown when breach of logic in domain object

    """

    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg
