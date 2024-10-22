# -*- coding: utf-8 -*-

"""
Exception management module

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'


class InvalidData(Exception):
    """
    Exception thrown when breach of data

    """

    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg


class InvalidNameError(Exception):
    """
    Exception thrown for invalid name

    """

    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg


class InvalidAddressError(Exception):
    """
    Exception thrown for invalid address

    """

    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg


class InvalidEmailError(Exception):
    """
    Exception thrown for invalid email address

    """

    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg


class InvalidPhoneNumberError(Exception):
    """
    Exception thrown for invalid phone number

    """

    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg


class InvalidMobilePhoneNumberError(InvalidPhoneNumberError):
    """
    Exception thrown for invalid mobile phone number

    """

    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg


class InvalidAmountError(Exception):
    """
    Exception thrown for invalid amount

    """

    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg


class InvalidCurrencyError(Exception):
    """
    Exception thrown for invalid currency

    """

    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg


class NoConnectionError(Exception):
    """
    Exception thrown for No response

    """

    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg


class TimeOutError(Exception):
    """
    Exception thrown when time out occurs

    """

    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg


class TrackingError(Exception):
    """
    Exception thrown when time out occurs

    """

    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg
