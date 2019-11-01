# -*- coding: utf-8 -*-

"""
Exception management module

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'


class NotFoundError(Exception):
    """
    Exception thrown when breach of logic in infrastructure layer

    """

    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg


class DomainError(Exception):
    """
    Exception thrown when breach of logic in domain object

    """

    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg
